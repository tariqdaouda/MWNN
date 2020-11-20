from sklearn.preprocessing import Normalizer
from sklearn.neighbors import kneighbors_graph, radius_neighbors_graph
from sklearn.metrics.pairwise import euclidean_distances, paired_distances
import numpy as np
import gc

class MWNN(object):
    """MWNN"""
    def __init__(self):
        super(WNN, self).__init__()
        self.modalities = {}
        self.weighted_similarities = 0
        
    def add_modality(self, values, name, neighbors_def, l2_normalize=False, use_radius=False, **sklearn_kwargs):
        """
        Add a modality to the store
           
           :param array values: The matrix of values representing the data
           :param str name: A name for the modality
           :param number neighbors_def: Either the number of neighbors or the radius to use
           :param bool l2_normalize: Weither the values should be normalized
           :param bool use_radius: Weither to use radius nn, if False will use KNN
           :param sklearn_kwargs: Arguments for sklearn neighbors function
        """
        if l2_normalize:
            values = Normalizer(norm="l2").fit(values).transform(values)
        
        if use_radius:
            fct = radius_neighbors_graph
        else:
            fct = kneighbors_graph
                
        self.modalities[name] = {
            "neighbors_def": neighbors_def,
            "values": values,
            "sklearn_kwargs": sklearn_kwargs,
            "neighbors_fct": fct
        }
        
    def _compute_SNN(self, adjancency, prune=1/20):
        """Compute similar nearest neighbors"""
        snn = adjancency * adjancency.T
        k = adjancency.shape[0]
        snn[ (snn /(k + (k - snn)) < prune)] = 0
        return snn
    
    def exp_dist(self, graph, values, first_neighbors, predictions, paired, eps=1e-5):
        """the main distance used to measur similarites between data points"""
        if paired:
            _d = paired_distances
        else :
            _d = euclidean_distances
            
        sig1 = self._compute_SNN(graph).sum(axis = 1) / 20
        up = _d(values, predictions) - _d(values, first_neighbors)
        up[up < 0] = 0
        return np.exp( -up / ( sig1 - _d(values, first_neighbors) + eps ) ).astype("float32")
    
    def _make_graphs(self):
        """compute graphs and adjancency matrices for all modalities"""
        print("0...")
        for name, dct in self.modalities.items():
            graph = dct["neighbors_fct"](
                dct["values"], dct["neighbors_def"], mode="distance", **dct["sklearn_kwargs"]
            ).toarray().astype("float32")
            self.modalities[name]["first_neighbors"] = dct["values"][graph.argmax(axis = 0)]
            graph[graph > 1] = 1
            self.modalities[name]["graph"] = graph
        
    def _get_pre_weights(self, eps=1e-5):
        """get the values used for weight computation"""
        ref_preds = {}
        pre_weights = {}
        pre_weights_sum = 0
        print("1...")
        for name, dct in self.modalities.items():
            ref_aff = None
            affinities = []
            for name2, dct2 in self.modalities.items():
                print("%sx%s" % (name, name2))
                preds = np.dot(dct2["graph"], dct["values"]) / dct2["neighbors_def"]
                mod_aff = self.exp_dist(dct2["graph"], dct["values"], dct["first_neighbors"], preds, True, eps)
                gc.collect()
                if name == name2:
                    ref_aff = mod_aff
                    ref_preds[name] = preds
                else:
                    affinities.append(mod_aff)
            affinities = np.array(affinities)
            pre_weights[name] = np.exp( ref_aff / ( np.sum(affinities, axis = 0) + eps) )
            pre_weights_sum += pre_weights[name]
            
        return pre_weights, pre_weights_sum, ref_preds
    
    def _make_similarities(self, pre_weights, pre_weights_sum, ref_preds, eps=1e-5) :
        """compute the final weighted similaries graph from pre-weights. This is the most memory heavy function"""
        print("2...")
        for name2, pre_weight in pre_weights.items():
            print("  ", name2)
            dct = self.modalities[name2]
            dct["weights"] = {}
            weight = pre_weight / pre_weights_sum
            dct["weights"][name2] = weight
            self.weighted_similarities += weight * self.exp_dist(dct["graph"], dct["values"], dct["first_neighbors"], ref_preds[name2], False, eps)
            gc.collect()
            
        self.weighted_similarities[self.weighted_similarities == 1] = 0

    def fit(self, eps=1e-5):
        """
        Add a modality to the store
           
           :param float eps: A small value to prevent division by 0
        """
        self._make_graphs()
        gc.collect()
        pre_weights, pre_weights_sum, ref_preds = self._get_pre_weights(eps=eps)
        gc.collect()
        return self._make_similarities(pre_weights, pre_weights_sum, ref_preds, eps=1e-5)

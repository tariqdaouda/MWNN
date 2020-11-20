# Multi-modal Weighted Nearest Neighbors

This is a python implementation of [Weighted Nearest Neighbors](https://www.biorxiv.org/content/10.1101/2020.10.12.335331v1) with some added features. WNN was introduced by Hao et al. in '__Integrated analysis of multimodal single-cell data__' as a method to integrate multi-modal single-cell data (CITE-Seq, ATAC-Seq, scRNA-Seq...) into a single space. I did my best to reimplement the method in the pre-print but keep in mind that the original method may change from now and and the final publication, that may create some discrepencies.

## Differences between MWNN and WNN
* Support for an arbitrary number of modalities, at the moment WNN supports only [two](https://github.com/satijalab/seurat/issues/3693)
* Possibility to use radius nearest neighbors instead of KNN

# How to use it
```python
  from mwnn.mwnn import MWNN
  
  rna_adata = sc.read("scRNASeq.h5ad")
  prot_adata = sc.read("CITESeq.h5ad")

  sc.pp.pca(rna_adata, n_comps=30)
  sc.pp.pca(prot_adata, n_comps=18)

  mwnn = MWNN()
  mwnn.add_modality(rna_adata.obsm["X_pca"], "rna", 20)
  mwnn.add_modality(prot_adata.obsm["X_pca"], "protein", 20)
  mwnn.fit()

  prot_adata.obsm["mwnn"] = wnn.weighted_similarities
  sc.pp.neighbors(prot_adata, use_rep="mwnn")
  sc.tl.umap(prot_adata)
```

# Installation

```
  git clone git@github.com:tariqdaouda/MWNN.git
  cd MWNN
  python setup.py
```

Alternatively you can just copy the mwnn.py in your current folder, altought I do not condone copy / pasting as it a sure way to maintenance hell.

# References
* [WNN paper: Integrated analysis of multimodal single-cell data](https://www.biorxiv.org/content/10.1101/2020.10.12.335331v1)
* [R implementation from the authors](https://github.com/satijalab/seurat)

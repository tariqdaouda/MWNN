from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='mwnn',

    version='0.1',

    description='Multi-modal Weighted Nearest Neighbors (MWNN)',
    long_description="""This is a python implementation of [Weighted Nearest Neighbors](https://www.biorxiv.org/content/10.1101/2020.10.12.335331v1) with some added features. WNN was introduced by Hao et al. as a method to integrate multi-modal single-cell data (CITE-Seq, ATAC-Seq, scRNA-Seq...) into a join space. I did my best to reimplement the method in the pre-print but keep in mind that the original method may change from now and and the final publication, that may create some discrepencies.""",
    url='',

    author='Tariq Daouda',
    author_email='',

    license='MIT',
    
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    python_requires='>=3.5',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],

    install_requires=["sklearn", "scipy", "numpy", "scanpy"],

    keywords='',

    packages=find_packages(),

    package_dir={'mwnn': 'mwnn'}
    # packages=['fiberedae']
)

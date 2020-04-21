""" seg1d:  Python module for automated 1D subsequence segmentation
Copyright (C) 2020  Mathew Schwartz
"""

from . _about import __version__
import os

from . segment import Segmenter, segmentData

__all__ = ['Segmenter', 'segmentData', 'sampleData']


def get_data_dir():
    """Returns the directory of the package.
    """
    return os.path.join(os.path.dirname(__file__), 'examples', 'data')


def sampleData(c=0.8):
    """ Helper function for accessing sample data.

    Parameters
    ----------

    c : float, optional
        the minimum correlation weights to load from the sample dataset

    """

    import numpy as np

    data_dir = get_data_dir()

    refWeights = np.load(data_dir+os.sep+'w.npy', allow_pickle=True)[()]
    refData = np.load(data_dir+os.sep+'r.npy', allow_pickle=True)
    targData = np.load(data_dir+os.sep+'t.npy', allow_pickle=True)[()]

    # define which weights to use
    refWeights = {x: y for x, y in refWeights.items() if y > c}

    return refData, targData, refWeights

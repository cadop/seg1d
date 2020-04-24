""" seg1d:  Python module for automated 1D subsequence segmentation
Copyright (C) 2020  Mathew Schwartz
"""

from . _about import __version__
import os

from . segment import Segmenter, segment_data

__all__ = ['Segmenter', 'segment_data', 'sampleData']


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

    refWeights = np.load(os.path.join(data_dir, 'w.npy'), allow_pickle=True)[()]
    refData = np.load(os.path.join(data_dir, 'r.npy'), allow_pickle=True)
    targData = np.load(os.path.join(data_dir, 't.npy'), allow_pickle=True)[()]

    # define which weights to use
    refWeights = {x: y for x, y in refWeights.items() if y > c}

    return refData, targData, refWeights

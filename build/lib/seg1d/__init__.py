'''
seg1d:  Python module for automated data segmentation
Copyright (C) 2020  Mathew Schwartz
Version: 0.0.8 (2020/3/20)
'''

__version__ = '0.0.8'

import os

from . segment import Segmenter, segmentData

__all__ = ['Segmenter', 'segmentData', 'sampleData']


def get_data_dir():
    '''Returns the directory of the package.

    '''

    dir_root     = os.path.dirname(__file__)
    dir_data     = os.path.join(dir_root, 'examples', 'data')

    return dir_data


def sampleData(c=0.8):
    '''Helper function for accessing sample data.

    Parameters
    ----------

    c : float, optional
        the minimum correlation weights to load from the sample dataset

    '''
    
    import numpy as np

    data_dir = get_data_dir()

    refWeights = np.load(data_dir+os.sep+'w.npy', allow_pickle=True)[()]
    refData = np.load(data_dir+os.sep+'r.npy', allow_pickle=True)
    targData = np.load(data_dir+os.sep+'t.npy', allow_pickle=True)[()]

    # define which weights to use
    refWeights = {x: y for x, y in refWeights.items() if y > c}

    return refData, targData, refWeights

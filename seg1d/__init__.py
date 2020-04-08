'''
seg1d:  Python module for automated data segmentation
Copyright (C) 2020  Mathew Schwartz
Version: 0.1 (2020/3/20)
'''

__version__ = '0.1'
import os

from . segment import Segmenter, segmentData

__all__ = ['Segmenter', 'segmentData', 'sampleData', 'get_data_dir']


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

    import pickle

    data_dir = get_data_dir()
    with open(data_dir+os.sep+'refData.pickle', 'rb') as f:
        refData = pickle.load(f)
    with open(data_dir+os.sep+'targData.pickle', 'rb') as f:
        targData = pickle.load(f)
    with open(data_dir+os.sep+'weights.pickle', 'rb') as f:
        refWeights = pickle.load(f)

    # define which weights to use
    refWeights = {x: y for x, y in refWeights.items() if y > c}

    return refData, targData, refWeights

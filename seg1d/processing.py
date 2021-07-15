'''
.. module:: processing
   :platform: Unix, Windows
   :synopsis: Utilities to process Features of time series data.
'''

from operator import itemgetter
from math import atan2
import itertools

from scipy import stats
import numpy as np

from . import algorithm as alg

class Features():

    @staticmethod
    def match_len(dataset):
        ''' interpolate to the maximum sized data in the reference set


        Parameters
        ----------

        dataset : List[Dict{feature:val}]
            list of multiple datasets containing dictionary of
            1d features that will be matched to same length


        Returns
        -------

        interp_d : List[Dict{feature:val}]
            feature length-matched data
        

        Notes
        -----

        Requires all features within each dataset to be of same length


        Examples
        --------

        >>> import numpy as np
        >>> import seg1d.processing as process
        >>> s20 = np.linspace(-np.pi*2, np.pi*2, 20) 
        >>> s30 = np.linspace(-np.pi*2, np.pi*2, 30)
        >>> s40 = np.linspace(-np.pi*2, np.pi*2, 40) 
        >>> s_longest = np.sin(s40)
        >>> a1 = {'s':np.sin(s20), 'c':np.cos(s20)}
        >>> a2 = {'s':np.sin(s30), 'c':np.cos(s30)}
        >>> a3 = {'s':s_longest, 'c':np.cos(s40)}
        >>> d = [a1, a2, a3]
        >>> r = process.Features.match_len(d)
        >>> print(len(r[0]['s']) == len(s_longest))
        True

        '''
        
        # Get the maximum length to interpolate others to 
        maxSize = -1
        for data in dataset:
            for arr in data.values():
                dataSize = len(arr)
                if dataSize > maxSize:
                    maxSize = dataSize

        # Interpolate each dataset
        interp_d = []
        for data in dataset:

            # Split feature dict to keys (1xn) and values (nxm)
            features = list( data.keys() )
            values = np.array(list( data.values() ))

            # Resample and recombine
            interped = alg.resample(values, maxSize)
            interp_d.append(dict(zip(features,interped)))

        return interp_d

    @staticmethod
    def center(ref_data):
        ''' subtract the mean of each feature from itself

        Parameters
        ----------

        ref_data : Dict{trial:Dict{feature:val}} or List[Dict{feature:val}]
            dictionary of 1d features that will be centered (mean subtracted) 

        Returns
        -------

        cent_dict : Dict{trial:Dict{feature:val}} or List[Dict{feature:val}]
            centered features

        Examples
        --------

        >>> import numpy as np
        >>> import seg1d.processing as process
        >>> s20 = np.linspace(-np.pi*2, np.pi*2, 10)
        >>> s30 = np.linspace(-np.pi*2, np.pi*2, 20) 
        >>> s1 = np.sin(s20)
        >>> c2 = np.cos(s30)
        >>> a1 = {'s1':s1+3, 'c1':np.cos(s20)+10}
        >>> a2 = {'s2':np.sin(s30)+15, 'c2':c2+15}
        >>> d = [a1, a2]
        >>> r = process.Features.center(d)
        >>> print( np.allclose(r[0]['s1'], (s1+3)- np.mean(s1+3), atol=1e-05) )
        True
        >>> print( np.allclose(r[1]['c2'], (c2+15)- np.mean(c2+15), atol=1e-05) )
        True

        '''

        # If it is is a dict of dicts
        if isinstance(ref_data, dict):
            cent_dict = {}
            for data in ref_data:
                cent_dict[data] = {}
                for marker, x in ref_data[data].items():
                    cent_dict[data][marker] = x-x.mean()
            return cent_dict

        # If its a list of dicts
        if isinstance(ref_data, (list, np.ndarray)):
            ref_cent = []
            for data in ref_data:
                cent_dict = {}
                for marker, x in data.items():
                    cent_dict[marker] = x-x.mean()
                ref_cent.append(cent_dict)

            return ref_cent

    @staticmethod
    def shared(D1, D2=None):
        ''' get data with only features shared amongst all sets

        Parameters
        ----------

        D1 : Dict{feature:value} or List[Dict{feature:value}]
            sets of references to be parsed for shared features

        D2 : Dict{feature:value} or List[Dict{feature:value}], optional
            optional dictionary, if supplied, will return as a secondary dict
            that also contains only shared features

        Returns
        -------

        d1 : same as input
            original data with only features shared by all inputs
        
        d1, d2 : same as input
            original data with only features shared by all inputs
        
        Notes
        -----

        This relies on proper feature labels. It cannot take arrays as there is no way
        to know what columns correspond to what features. 

        Examples
        --------

        >>> import seg1d.processing as process
        >>> d1 = {'a':[1,2], 'b':[2,2]}
        >>> d2 = {'e':[3,2], 'b':[5,1], 'a':[5,5]}
        >>> d3 = {'b':[8,2], 'a':[3,3], 'c': [1,2]}
        >>> r1, r2 = process.Features.shared(d1,[d2,d3])
        >>> print({k:r1[k] for k in sorted(r1)})
        {'a': [1, 2], 'b': [2, 2]}
        >>> print({k:r[k] for r in r2 for k in sorted(r)})
        {'a': [3, 3], 'b': [8, 2]}

        '''

        # get shared keys through overloaded intersection operator &
        shared_keys = {}
        if isinstance(D1, dict):
            shared_keys = D1.keys()

        elif isinstance(D1, (list, np.ndarray)):
            for i, data in enumerate(D1):
                if i == 0:
                    shared_keys = data.keys()
                shared_keys = shared_keys & data.keys() 

        # Check type of secondary input, if provided
        if isinstance(D2, dict):
            shared_keys = shared_keys & D2.keys()

        elif isinstance(D2, (list, np.ndarray)):
            d2_keys = {}
            for i, data in enumerate(D2):
                if i == 0:
                    d2_keys = data.keys()
                d2_keys = d2_keys & data.keys() 

            shared_keys = d2_keys & shared_keys
        
        # rename 
        x_labels = shared_keys

        if isinstance(D1, dict):
            d1_shared = { k:D1[k] for k in x_labels}

        elif isinstance(D1, (list, np.ndarray)):
            # TODO double check this is deterministic order
            # get the nxm arrays for each dataset
            # x = [ itemgetter(*x_labels)(i[1]) for i in D1.items() ]  # legacy method of Dict{Dict}
            # d1_shared = { k[0] : dict(zip(x_labels, x[i])) for i, k in enumerate(D1.items()) }
            x = [ itemgetter(*x_labels)(i) for i in D1 ] 
            d1_shared = [ dict(zip(x_labels, x[i])) for i, _ in enumerate(D1) ]

        # If there is no secondary data, return just the first one
        if D2 is None:
            return d1_shared

        # If a secondary dict was supplied, parse and return it as well
        if isinstance(D2, dict):
            d2_shared = { k:D2[k] for k in x_labels}

        elif isinstance(D2, (list, np.ndarray)):
            # TODO double check this is deterministic order
            # get the nxm arrays for each dataset
            x = [ itemgetter(*x_labels)(i) for i in D2 ] 
            d2_shared = [ dict(zip(x_labels, x[i])) for i, _ in enumerate(D2) ]

        return d1_shared, d2_shared


    @staticmethod
    def gen_weights(dataset):
        ''' Create weight table from reference data

        Parameters
        ----------

        dataset: List[Dict{feature:value}]
            sets of references to be correlated against eachother to generate 
            an importance score of each feature


        Returns
        -------

        weights : Dict{feature:score}
            normalized sum of weights over all segments 
        
        Notes
        -----

        All features should be of same length. 

        See Also
        --------

        match_len : match length of all features

        Examples
        --------

        >>> import numpy as np
        >>> import seg1d.processing as process
        >>> e10 = np.linspace(-np.pi*2, np.pi*2, 10)
        >>> s1 = {'f1': np.sin(e10) , 'f2': np.sin(e10), 'f3': np.linspace(0,9,10) }
        >>> s2 = {'f1': np.sin(e10) , 'f2': np.cos(e10), 'f3': -1*np.linspace(0,9,10) }
        >>> s3 = {'f1': np.sin(e10) , 'f2': np.tan(e10), 'f3': np.ones((10))}
        >>> d = [s1, s2, s3]
        >>> r = process.Features.gen_weights(d)
        >>> print([np.around(r[x], 3) for x in sorted(r)])
        [array([1.]), array([-0.25]), array([-1.])]

        '''

        # Get labels
        labels = [ m for v in dataset for m in v.keys() ]
        x_labels = set(labels)
        # # get the nxm arrays for each dataset
        x = [ list(itemgetter(*x_labels)(i)) for i in dataset ] 

        C = np.zeros((len(x_labels),1))

        cor_combinations = list(itertools.combinations(range(len(x)),2))

        for x1, x2 in cor_combinations:
            # get the correlations
            _corr = np.zeros((len(x_labels),1))
            for i in range(len(x[x1])):
                _corr[i] = stats.pearsonr(x[x1][i], x[x2][i])[0]
            # sum results
            C = np.nansum([C, _corr], axis=0)

        #scale between values
        minX = np.nanmin(C) # min of all values
        maxX = np.nanmax(C) # max of all values
        a = -1
        b = 1
        x_norm = a+ ((C- minX)*(b-a)) / (maxX - minX) # normalized on each element

        weights = dict(zip(x_labels, x_norm))

        return weights


    @staticmethod
    def meaningful(weights, limit=0.5, top=1000, include_keys=[]):
        ''' get a weight table of the most meaningful features

        Parameters
        ----------

        weights : Dict{feature:score}


        limit : float, optional {0.5}
            minimum threshold to include in weight table

        top : int, optional {1000}
            after sorting by most relevant, return only the top number of features

        include_keys : List[str], optional
            if provided, uses only the provided keys for the returned weight table. 
            This is useful for ensuring the weight table only includes keys available in 
            target and reference data. 


        Returns
        -------

        weight_table : Dict{feature:score}


        Notes
        -----

        Considers negative correlation as 'not important'. 


        Examples
        --------

        >>> import seg1d.processing as process
        >>> w = {'a': 0.1, 'b': 0.4, 'c': 0.2, 'd':0.8, 'e':0.9}
        >>> r = process.Features.meaningful(w, limit=0.1)
        >>> print(r)
        {'e': 0.9, 'd': 0.8, 'b': 0.4, 'c': 0.2}
        >>> r = process.Features.meaningful(w, limit=0.1, top=2)
        >>> print(r)
        {'e': 0.9, 'd': 0.8}
        >>> r = process.Features.meaningful(w, limit=0.1, include_keys=['a','b','d'])
        >>> print(r)
        {'d': 0.8, 'b': 0.4}

        '''

        # Pull out desired keys
        if len(include_keys) > 0:
            weights = {x:y for x,y in weights.items() if x in include_keys} # TODO Test this

        # TODO why does this change result?
        weights = {x:y for x,y in weights.items() if y>limit}

        # Sort 
        sorted_weights = { k: v for k, v in sorted(weights.items(), key=lambda x: x[1], reverse=True) if v>limit }

        # Slice top
        crop_weights = list(sorted_weights.items())[:top]
        
        # Return list converted back to dict
        return dict(crop_weights)


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

        dataset : List[dataset : Dict{feature : val}]
            list of multiple datasets containing dictionary of
            1d features that will be matched to same length


        Returns
        -------

        interp_dict : Dict{ dataset : Dict{feature : val}}
            feature length-matched data
        

        Notes
        -----

        Requires all features within each dataset to be of same length


        Examples
        --------

        >>> import segld.processing as process
        >>> a = process.Features.match_len()

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
        '''

        Parameters
        ----------

        ref_data : Dict{trial : Dict{feature : val}} or List[Dict{feature : val}]
            dictionary of 1d features that will be centered (mean subtracted) 

        Returns
        -------

        cent_dict : Dict{trial : Dict{feature : val}} or List[Dict{feature : val}]
            centered features

        Examples
        --------

        >>> import segld.processing as process
        >>> a = process.Features.center()

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

        D1 : Dict{feature : value} or List[Dict{feature : value}]
            sets of references to be parsed for shared features

        D2 : Dict{feature : value} or  List[Dict{feature : value}], optional
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

        >>> import segld.processing as process
        >>> a = process.Features.shared()

        '''

        # TODO this can be a list instead of a dict since we ignore the trial labels 
        # but doing so makes the dict/list check less reliable 

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
        """ Create weight table from reference data

        Parameters
        ----------

        dataset: List[ Dict{feature : value} ]
            sets of references to be correlated against eachother to generate 
            an importance score of each feature


        Returns
        -------

        weights : Dict{feature : score}
            segment weights
        

        Examples
        --------

        >>> import segld.processing as process
        >>> a = process.Features.gen_weights()

        """

        # Get labels
        x_labels = set({ m for v in dataset for m in v.keys()})
        # x_labels = set({ m for k,v in dataset.items() for m in v.keys()})
        # # get the nxm arrays for each dataset
        x = [ itemgetter(*x_labels)(i) for i in dataset ] 
        # x = [ itemgetter(*x_labels)(i[1]) for i in dataset.items() ] 

        C = np.empty((len(x_labels),1))

        cor_combinations = itertools.combinations(range(len(x)),2)
        for x1, x2 in cor_combinations:
            # get the correlations
            _corr = np.empty((len(x_labels),1))
            for i in range(len(x[x1])):
                _corr[i] = stats.pearsonr(x[x1][i], x[x2][i])[0]
            # sum results
            C += _corr  # TODO what happens when summing a nan value?
        
        #scale between values
        minX = min(C) # min of all values
        maxX = max(C) # max of all values
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

        weights : Dict{feature : score}


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

        weight_table : Dict{feature : score}


        Notes
        -----

        Considers negative correlation as 'not important'. 


        Examples
        --------

        >>> import segld.processing as process
        >>> a = process.Features.meaningful()

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


    @staticmethod
    def align_direc(data):
        ''' align spatial features to vector
        

        Parameters
        ----------



        Returns
        -------


        Notes
        -----

        This concept requires an nxm feature list to be organized in strides of 3 for xyz values. 

        Examples
        --------

        >>> import segld.processing as process
        >>> a = process.Features.align_direc()

        '''

        def get_mid(data, label_1, label_2):
            ''' get the midpoint of two marker names by breaking into tuple
            '''

            x = ( data[(label_1,'x')] + data[(label_2,'x')] ) /2.0
            y = ( data[(label_1,'y')] + data[(label_2,'y')] ) /2.0
            z = ( data[(label_1,'z')] + data[(label_2,'z')] ) /2.0

            return x,y,z

        #get the pelvis direction in the lab coordinate
        try:
            p1_p2 = get_mid(data,'RASIS', 'LASIS')
            p3_p4 = get_mid(data,'RICR', 'LICR')

        except:
            p1_p2 = get_mid(data,'RASI', 'LASI')
            p3_p4 = get_mid(data,'RPSI', 'LPSI')

        p1_p2 = np.array(p1_p2).T
        p3_p4 = np.array(p3_p4).T

        # get direction vector   # Shape = (~1014,3)
        v = p3_p4 - p1_p2  

        # normalize vector        
        xSize = np.shape(v)[0]
        angle = np.empty((xSize,))
        for i in range(0,xSize):
            norm = np.linalg.norm(v[i])
            if norm == 0: newDirec = v[i]
            else: newDirec =  v[i] / norm
            a = [0,1]
            b = newDirec
            angle[i] = atan2(b[1],b[0]) - atan2(a[1],a[0]) 

        # Data keys
        keys = data.keys()
        x = np.array(list(data.values()), dtype=float).T

        rSize =  np.shape(x)[0] 
        cSize = np.shape(x)[1]
        cSize = np.int(cSize/3)
        rot = np.empty((rSize,cSize*3))
        
        for i in range(0,rSize):
            theta = -1*angle[i]
            Rpel = np.array([[np.cos(theta), -np.sin(theta),0 ],
                            [np.sin(theta), np.cos(theta) ,0 ],
                            [0,             0,             1 ]],dtype=np.float64)

            for j in range(0,cSize):
                k = j*3
                m = [ x[i][k], x[i][k+1], x[i][k+2] ]
                mNew = np.dot(Rpel,m)
                rot[i][k]=mNew[0]
                rot[i][k+1]=mNew[1]
                rot[i][k+2]=mNew[2]

        norm_data = rot.T
        norm_dict = dict(zip(keys, norm_data))
        return norm_dict


 
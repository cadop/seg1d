'''
.. module:: segment
   :platform: Unix, Windows
   :synopsis: Segmentation of 1D data from subsequences.

'''

from copy import deepcopy

import numpy as np

from . import algorithm as alg


class Segmenter:
    '''
    Segmentation class that exposes all algorithm parameters and attributes for
    advanced access and tuning of segmentation.

    Additional convenience methods for adding reference and target data as
    numpy arrays are provided.

    Results of each step of the algorithm process can be accessed through the
    class Attributes after running the segmentation. These can likewise be
    passed to the algorithms methods described in the documentation.


    Examples
    --------
    Simple usage of the class by directly assigning attributes
    using sample data included with this package.

    >>> import seg1d
    >>> import numpy as np
    >>> 
    >>> #Make an instance of the segmenter
    >>> s = seg1d.Segmenter()
    >>> 
    >>> #retrieve the sample reference, target, and weight data
    >>> s.r,s.t,s.w = seg1d.sampleData()
    >>> 
    >>> #set the parameters
    >>> s.minW,s.maxW,s.step = 70, 150, 1
    >>>
    >>> np.around(s.segment(), decimals=7)
    array([[207.       , 240.       ,   0.9124224],
           [342.       , 381.       ,   0.8801901],
           [ 72.       , 112.       ,   0.8776795]])
    '''

    def __init__(self):
        ''' Initialization of segmentation class and parameters


        Attributes
        ----------

        r : array of dicts
            The reference dataset
        t : dict
            The target dataset
        w : dict
            Weights for correlation

        minW : int
            minimum percent to scale data
        maxW : int
            maximum percent to scale data
        step : int
            step size for rolling correlation
        wSizes : list
            sizes to use for resampling reference
            (can be used instead of minW,maxW,step)
        cMax : bool
            use maximum in rolling correlation (default False)
        cMin : float
            -1 to 1, min correlation
        cAdd : float
            0 to 1 or None, value to add for forcing clusters (Default 0.5)
        pD : None
            peak distance to use for scipy peak detection (Default None)
        nC : int
            number of clusters for correlation results
        fMode : {'w', 'm', 's'}
            keyword to use for aggregating feature correlations (default `w`).
            Options, w=weighted mean, m=mean, s=sum
        fScale : bool
            scale the feature correlation by its weight before feature
            aggregation (Default True)

        tSeg : []    
            the target data as segmented arrays

        '''
        # internal attributes
        # tLen : int
        #     length of target data
        # rLen : int
        #     length of reference data
        # tF : set
        #     features of the target data
        # rF : set
        #     features of the reference data
        # wF : set
        #     features of the weights

        # '''

        self.r = []    # reference data ## if 'r' not in *args
        self.t = {}    # target data
        self.w = {}    # weights

        self.tF = set()  # features of the target data
        self.rF = set()  # features of the reference data
        self.wF = set()  # features of the weights

        self.tLen = 0      # length of target data
        self.rLen = 0      # length of reference data

        self.minW = 50     # minimum percent to scale data
        self.maxW = 200    # maximum percent to scale data
        self.step = 1      # step size for rolling correlation
        self.wSizes = []     # sizes to use for resampling reference

        self.cMax   = False  # use maximum in rolling correlation
        self.cMin   = 0.5    # min correlation
        self.cAdd   = 0.5    # value to add for forcing clusters
        self.pD     = None   # peak distance
        self.nC     = 2      # num clusters
        self.fMode  = 'm'    # method to aggregate weighted features
        self.fScale = True   # scale the features correlation by the weight

        self.tSeg   = []     # the target data as segmented arrays

        self._maxR  = 0      # keeps track of reference size


    @property
    def featC(self):
        '''Rolling correlation of reference and target features created by
        :func:`algorithm.rollingWinCorr`
        '''

        resDict = {}
        # iterate through a change in percentage of window sizes
        for wSize in self.wSizes:
            featDict = {}
            # for using generated tuples
            for featName in self.w:
                # make an array of the reference data
                r = np.asarray([x[featName] for x in self.r])

                # get target data of this feature
                t = self.t[featName]

                # get the correlation of a reference set across the length of
                # the target data
                featDict[featName] = alg.rollingWinCorr(t, r, wSize, cMax=self.cMax) 

            # store features for this window size
            resDict[wSize] = featDict

        return resDict


    @property
    def peaks(self):
        ''' Peaks of the correlations created by :func:`algorithm.getPeaks`
        '''
        return alg.getPeaks(self.meanC, self.cMin, self.pD)


    @property
    def meanC(self):
        ''' The averaged correlation of the rolling feautre correlation
        and the weighting table created by :func:`algorithm.avrCorrelate`
        '''
        return alg.avrCorrelate(self.featC, self.w, self.fMode, self.fScale)


    @property
    def clusters(self):
        '''Segments reduced by clustering algorithm from
        :func:`algorithm.clusterSegments`
        '''
        return alg.clusterSegments(self.groups, segAdder=self.cAdd, nClust=self.nC)


    @property
    def groups(self):
        ''' Possible segments through parsing overlapping segment locations
        defined by :func:`algorithm.uniqSegments`
        '''
        return alg.uniqSegments(self.peaks, self.tLen)


    @property
    def masked_t(self):
        ''' The target data as ndarray masked with the non-defined
        segments as NaNs.

        Useful for plotting, but should not be used for data processing as
        dicts are not ordered.
        '''

        # slice and mask the data
        _t = np.asarray([x for x in self.t.values()])
        mask_seg = np.concatenate([np.arange(x[0], x[1], 1)
                                   for x in self.clusters])
        mask_arr = np.full(_t.shape, True, dtype=bool)
        mask_arr[ :, mask_seg] = False
        _t[mask_arr] = np.NaN

        return _t

    def _processParams(self):
        ''' Processes parameters

        If sizes for scaling are not set, uses min,max,step parameter.
        If no weights were set, a default of 1 (no weighting) will be applied.

        '''

        self._refSize()

        if len(self.w.keys()) == 0: self.w = {x: 1 for x in self.t.keys()} 

        self.wF = set(self.w.keys())
        self.tF = set(self.t.keys())

        for _r in self.r: self.rF.update(_r.keys())

        self._interpRef()

        self.tLen = len(list(self.t.values())[0])

        if len(self.wSizes) == 0:
            self._setScales()

        self._checkCompliance()


    def _checkCompliance(self):
        ''' Checks data formats and parameters for compliance with
        segmentation methods
        '''

        assert 0 not in self.wSizes, "Scaling parameters cannot have 0"
        assert self.minW < self.maxW, "Minimum scaling must be less than Maximum"
        assert len(self.r) > 0, "Must have at least one reference"
        assert len(self.t.values()) > 0, "Must have one target"
        assert self.wF.issubset(self.tF), "All weights must exist in target data"
        assert self.wF.issubset(self.rF), "All weights must exist in reference data"

    def _refSize(self):
        ''' Find the max length of all reference data
        '''

        def d(x): return max([ len(y) for y in x.values() ])
        def a(x): return max([ d(y) for y in x ])

        self._maxR = a(self.r)
        self.rLen = a(self.r)

    def _setScales(self):
        ''' Sets the window scaling sizes based on the min and 
        max percent with the step size 
        '''

        # define steps for data scaling based on percentage
        wScale = range(self.minW, self.maxW+1, self.step)
        self.wSizes = set([ int( self.rLen* (x/100.0) ) for x in wScale ])

    def _interpRef(self):
        ''' Resamples reference data to match the same length
        '''

        _r = deepcopy(self.r)

        for ref in _r:
            for f in ref:
                ref[f] = alg.resample(ref[f], self._maxR)[0]

        self.r = _r


    def setTarget(self, t, copy=True):
        ''' Sets the target data by overiding any existing target.
        If the target is not a dict, it will be converted to one.

        Parameters
        ----------
        t : dict or ndarray
            | Dictionary containing labeled features as keys and values as 1-D
              arrays (must be same size).
            | ndarray of dimension 1 will be used as a single feature
              for the target.
            | ndarray of n-dimensions will use rows as unique features.

        copy : bool, optional
            If True, will make a deepcopy of the passed parameter (Default True)


        Returns
        -------
        None


        See Also
        --------
        addReference : Add a reference item


        Notes
        -----
        This is the recommended method for adding a feature.
        You can also set the target directly through the
        Attribute *t* by ```Segmenter.t =  ```
        however, this method ensures the data labels and length or stored
        properly.
        Setting *t* directly must be done with a dictionary.


        Examples
        --------

        Target data can be set to a single numpy array.

        >>> import numpy as np
        >>> import seg1d
        >>> 
        >>> S = seg1d.Segmenter()
        >>> t = np.linspace(0,1,4)
        >>> S.setTarget(t)
        >>> S.t
        {'0': array([0.        , 0.33333333, 0.66666667, 1.        ])}

        Alternatively, you can pass a 2-dimensional array representing
        multiple features.

        >>> S = seg1d.Segmenter()
        >>> t = np.linspace(0,1,6).reshape(2,3)
        >>> S.setTarget(t)
        >>> S.t
        {'0': array([0. , 0.2, 0.4]), '1': array([0.6, 0.8, 1. ])}

        '''

        assert isinstance(t, (dict, list, np.ndarray)), \
                          'Target must be Dict, List, or Array'

        if copy:
            t = deepcopy(t)
            self.t = deepcopy(self.t)

        if not isinstance(t, dict):

            if t.ndim == 1:
                self.t = {'0': t}

            else:
                _tD = {}
                for i, _t in enumerate(t):

                    _tD[str(i)] = _t

                self.t = _tD
        
        else: self.t = t

        self.tLen = len(list( self.t.values() )[0])
        self.tF   = set(self.t.keys())


    def addReference(self, r, copy=True):
        ''' Appends a reference containing one or more features to the existing
        reference dataset.
        If the reference is not a dict, it will be converted to one.
        If this should be the only reference set, use ``clearReference()``
        before calling this method.


        Parameters
        ----------
        r : dict or ndarray
            | Dictionary containing labeled features as keys and values as
              1-D arrays (must be same size).
            | ndarray of dimension 1 will be used as a single feature for the
              reference.
            | ndarray of n-dimensions will use rows as unique features.

        copy : bool, optional
            If True, will make a deepcopy of the passed parameter
            (Default True).


        See Also
        --------
        setTarget : Set the target data
        clearReference: Clear the current reference data


        Notes
        --------
        This method allows features that are not in previous references to be
        added, and vice-versa.
        It will also allow different sizes of reference data to be added.
        This is done as you can explicitly declare which features to use when
        segmenting.


        Examples
        --------

        Add a reference with multiple features

        >>> import seg1d
        >>> import numpy as np
        >>> 
        >>> S = seg1d.Segmenter()
        >>> r = np.linspace(0,1,6).reshape(2,3)
        >>> S.addReference( r )
        >>> S.r
        [{'0': array([0. , 0.2, 0.4]), '1': array([0.6, 0.8, 1. ])}]

        Alternatively, each row of the array can be added as the same labeled
        feature for different references by calling this method in a loop.
        Notice this is now an array of dictionaries containing the same
        feature label.

        >>> S = seg1d.Segmenter()
        >>> r = np.linspace(0,1,6).reshape(2,3)
        >>> for _r in r: S.addReference(_r)
        >>> S.r
        [{'0': array([0. , 0.2, 0.4])}, {'0': array([0.6, 0.8, 1. ])}]


        '''

        assert isinstance(r, (dict, np.ndarray)), \
                          'Reference must be Dict or Array'

        if copy:
            r = deepcopy(r)
            self.r = deepcopy(self.r)

        if not isinstance(r, dict):

            if r.ndim == 1:
                self.r.append({'0': r})
                self.rF.add('0')

            else:
                _rD = {}
                for i, _r in enumerate(r):

                    _rD[str(i)] = _r

                self.r.append(_rD)
                self.rF.update(_rD.keys())

        else:
            self.r.append(r)
            self.rF.update(r.keys())


    def clearReference(self):
        ''' Removes any reference data currently assigned

        Parameters
        ----------
        None


        Returns
        -------
        None


        See Also
        --------
        addReference: Add a reference item


        Notes
        -----
        This method also clears the `rF`, and `rLen` attributes.

        Examples
        --------
        >>> import numpy as np
        >>> import seg1d
        >>>
        >>> S = seg1d.Segmenter()
        >>> S.addReference( np.linspace(0,3,3) )
        >>> S.r
        [{'0': array([0. , 1.5, 3. ])}]
        >>> S.clearReference()
        >>> S.r
        []

        '''

        self.r = []
        self.rF = set()
        self.rLen = 0
        self._maxR = 0

    def makeSegments(self):
        ''' Returns an array of segmented target data

        Parameters
        ----------
        None

        Returns
        -------
        Segments : List[Dict[str,numpy.array]]
            applies the segment endpoints to the given target data *t* on all
            features.

        Examples
        --------
        >>> import numpy as np
        >>> import seg1d

        >>> #create an array of data
        >>> x = np.linspace(-np.pi*2, np.pi*2, 500)
        >>> #get an array of data from a sin function
        >>> targ = np.sin(x)

        >>> #Make an instance of the segmenter
        >>> S = seg1d.Segmenter()
        >>> #set scaling parameters
        >>> S.minW,S.maxW,S.step = 98, 105, 1
        >>> #Set target and reference data
        >>> S.setTarget(targ)

        >>> #define a segment within the sine wave to use as reference
        >>> S.addReference(targ[75:100])
        >>> #call the segmentation algorithm
        >>> segments = S.segment()
        >>> np.around(segments, decimals=7)
        array([[ 75.       , 100.       ,   1.       ],
               [324.       , 348.       ,   0.9999992]])

        >>> S.makeSegments()
        [{'0': array([0.94988243, 0.94170965, 0.93293968, 0.92357809, 0.91363079,
               0.90310412, 0.89200474, 0.88033969, 0.86811636, 0.85534252,
               0.84202625, 0.82817601, 0.81380058, 0.79890907, 0.78351093,
               0.76761592, 0.75123412, 0.73437593, 0.71705202, 0.6992734 ,
               0.68105132, 0.66239735, 0.64332332, 0.62384133, 0.60396372])}, {'0': array([0.95374324, 0.94587102, 0.93739898, 0.92833248, 0.91867727,
               0.90843947, 0.89762559, 0.88624247, 0.87429733, 0.86179776,
               0.84875167, 0.83516734, 0.82105338, 0.80641875, 0.79127273,
               0.77562491, 0.75948523, 0.74286391, 0.72577151, 0.70821885,
               0.69021707, 0.67177759, 0.6529121 , 0.63363256])}]
        '''

        self.tSeg = []

        for c in self.clusters:
            self.tSeg.append({ x: y[c[0]:c[1]] for x, y in self.t.items() })

        return self.tSeg

    def segment(self):
        ''' Method to run the segmentation algorithm on the current
        Segmenter instance

        Parameters
        ----------

        None


        Returns
        -------

        *3 x n* array
            segments of form
            ``[start of segment,end of segment,correlation score]``


        Examples
        --------

        This example is the same as the main ``Segmenter`` class as it is the
        interface method.

        >>> import seg1d
        >>>
        >>> #Make an instance of the segmenter
        >>> s = seg1d.Segmenter()
        >>> 
        >>> #retrieve the sample reference, target, and weight data
        >>> s.r,s.t,s.w = seg1d.sampleData()
        >>> 
        >>> #set the parameters
        >>> s.minW,s.maxW,s.step = 70, 150, 1
        >>>
        >>> s.segment()
        [[207, 240, 0.9124223704844657], [342, 381, 0.880190111545897], [72, 112, 0.8776795468035664]]

        '''

        self._processParams()   # generate missing parameters

        return self.clusters


def segmentData(r, t, w, minS, maxS, step):
    ''' Segmentation manager for interfacing with Segmenter class

    Find segments of a reference dataset in a target dataset using
    a rolling correlation of *n* number of reference examples with
    a peak detection applied to the average of *m* reference features
    with weights applied to each feature.

    Parameters
    ----------
    r : List[Dict[key,numpy.array]]
        reference data of form
        ``[ {(feature Key): [data array] }, {(feature Key): [data array] } ]``

    t : Dict[key,numpy.array]
        target data of form
        ``{ (feature Key): [data array] }``

    w : Dict[key,float] or None
        Weights of form
        ``{ (feature key):float,(feature key):float }``

    minS : int
        Minimum scale to apply for reference data

    maxS : int
        Maximum scale to apply for reference data

    step : int
        Size of step to use in rolling correlation

    Returns
    -------
    *3 x n* array
        segments of form
        ``[start of segment,end of segment,correlation score]``

    Examples
    --------
    First we import sample data from the examples folder that has multiple
    features derived from motion capture data

    >>> import seg1d
    >>> r,t,w = seg1d.sampleData()

    Then we define some segmentation parameters such as the scaling percentage
    of the reference data and index stepping to use in rolling correlation

    >>> minW = 70 # percent to scale down reference data
    >>> maxW = 150 # percent to scale up reference data
    >>> step = 1 #step to use for correlating reference to target data

    Finally we call the segmentation algorithm

    >>> seg1d.segmentData(r,t,w,minW,maxW,step)
    [[207, 240, 0.9124223704844657], [342, 381, 0.880190111545897], [72, 112, 0.8776795468035664]]


    '''

    # Make an instance of the segmenter
    s = Segmenter()

    # set the parameters
    s.minW = minS
    s.maxW = maxS
    s.step = step
    s.t = t
    s.r = r
    s.w = w

    # return the segments created by the Segmenter
    return s.segment()

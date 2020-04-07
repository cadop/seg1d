'''
.. module:: algorithm
   :platform: Unix, Windows
   :synopsis: Algorithms to handle segmentation of 1D sub-series data.

'''

from operator import itemgetter
from copy import deepcopy
import warnings

import numpy as np
from scipy import signal
from scipy.signal import find_peaks
from scipy.interpolate import interp1d
from sklearn.preprocessing import minmax_scale 
from sklearn.cluster import AgglomerativeClustering

from . import optimized_funcs as optf


def rollingWinCorr(x,yData,winSize,cMax=False):
    '''
    Rolling Correlation
    
    Calculates the rolling correlation coefficient over the given window sizes
    
    Parameters
    ----------
    x : 1-D array
        array of target data 
    
    yData : 2-D array
        array of reference data
    
    winSize : int
        scale of the that the reference data should be rescaled to 

    Other Parameters
    ----------------
    cMax : Bool, optional
        Use maximum of correlations (Default False)

    Returns
    -------
    ndarray
        1-D array of length (size(x) - winSize + 1)
    
    Warnings
    --------
    | The reference data (yData) must be smaller than the target data (x) AFTER resampling.
    | This means if the reference data is length 80, and the target data is length 100, 
     it will work. However, if the winSize is supposed to be length 120, the reference
     will be scaled and correlation will crash.


    See Also
    --------

    avrCorrelate : (takes the return of this function)


    Examples
    --------

    >>> import numpy as np
    >>> import seg1d.algorithm as alg

    >>> #make waves
    >>> x = np.sin( np.linspace(-np.pi*1, np.pi*1, 20) )
    >>> y = np.sin( np.linspace(-np.pi*2, np.pi*2, 80) ).reshape(4,20)

    >>> #apply rolling correlations with 10 and 15
    >>> alg.rollingWinCorr(x, y, 10 )
    array([-0.00766151,  0.02078156,  0.03501678,  0.04019572,  0.04211895,
            0.04262637,  0.04211895,  0.04019572,  0.03501678,  0.02078156,
           -0.00766151])
    >>> alg.rollingWinCorr(x, y, 15 )
    array([0.03321832, 0.03972237, 0.04254858, 0.04254858, 0.03972237,
           0.03321832])

    '''

    refScaled = resample(yData,winSize) #resample reference data

    #get the rolling correlation between reference(s) and target
    rCorr = optf.rCor(x,refScaled)

    #stack the correlations 
    corrs = np.vstack(rCorr)

    #return the mean or max of the correlations of the references 
    if cMax : return np.max(corrs,axis=0)
    else : return np.mean(corrs,axis=0)  


def avrCorrelate(x,w,method='m',scale=True):
    '''
    Average Weighted Correlation

    Takes in the correlated data results and multiply the weighting values
    to each array of data for that feature. 
    | Averages the results of the weighted features
    

    Parameters
    ----------
    x : dict of dicts containing arrays
            ``{scale:{ feature: array([correlations]) } }``
        
    w : dict of floats
            ``{ feature: weight }``

    method : string, optional
        keyword to use for aggregating feature correlations (default `w`).
        Options, w=weighted mean, m=mean, s=sum
    
    scale : bool, optional
        keyword argument for scaling the correlated feature before applying 
        any of the aggregation methods

    Returns
    -------

    dict of arrays ``{scale: array([weighted correlations]) }``
    

    See Also
    --------

    rollingWinCorr : (input for this function)
    getPeaks : (takes the return of this function)


    Examples
    --------

    >>> import random
    >>> import numpy as np
    >>> import seg1d.algorithm as alg

    >>> #make a convenience function to get a wave for sample data
    >>> def s(f1, f2, f3): return np.sin( np.linspace(f1, f2, f3) )

    >>> x = {
    ...     10: {'a': s(-np.pi*0.8, 0, 10), 'b': s(0, np.pi*0.8, 10)},
    ...     20: {'a': s(-np.pi*0.7, 0, 10), 'b': s(0, np.pi*0.7, 10)}
    ... }

    Assign some weights and find the averaged value

    >>> w = { 'a': 0.5, 'b': 0.9 }
    >>> a = alg.avrCorrelate(x, w )
    >>> for k,v in a.items(): print(k,v)
    10 [-0.14694631 -0.07296588  0.00666771  0.0857847   0.15825538  0.21846498
      0.26174865  0.28475292  0.2856955   0.26450336]
    20 [-0.20225425 -0.12293111 -0.03630481  0.0524783   0.13814375  0.21560229
      0.2802522   0.32825274  0.35675226  0.36405765]

    Change the weight values and see the weighted scores change

    >>> w = { 'a': 0.9, 'b': 0.2 }
    >>> a = alg.avrCorrelate(x, w )
    >>> for k,v in a.items(): print(k,v)
    10 [-0.26450336 -0.3270411  -0.36424081 -0.37322037 -0.35328408 -0.30597655
     -0.23496298 -0.14574528 -0.04523573  0.05877853]
    20 [-0.36405765 -0.39304054 -0.39867347 -0.38062179 -0.33995792 -0.27909765
     -0.20165658 -0.1122354  -0.01614647  0.0809017 ]

    '''

    cDict = {}

    #iterate through window sizes of data
    for win in x:      
        winData = x[win]
        w_list = []
        featRes = []
        #iterate through features of data
        for f in winData:
            featData = winData[f]
            #multiply weights from the table to scale features
            if scale: featRes.append( w[f] * featData )
            else: featRes.append( featData )
            w_list.append(w[f])
        
        #stack numpy arrays and average correlations on each frame 
        sF = np.vstack(featRes)
        if method=='m': cDict[win] = np.mean(sF,axis=0)
        if method=='w': cDict[win] = np.average(sF,axis=0,weights=w_list)
        if method=='s': cDict[win] = np.sum(sF,axis=0)

    return cDict


def getPeaks(x,minC= 0.7,dst=None):
    '''
    Peak Detection

    Find the peaks of a data array with a minimum value of a peak
    and an optional distance parameter. 

    Relies on ``scipy.signal.find_peaks``

    Parameters
    ----------

    x : dict containing 1d arrays
        ``{scale:  [correlations] }``
        

    Other Parameters
    ----------------

    minC : float, optional
        -1 to 1

    dst : number, optional
        int or float

    Returns
    -------
    n x 3 array 
        sorted by highest to lowest correlation of form 
        ``[ scale, correlation , peak index ]``
    

    See Also
    --------

    avrCorrelate : (input for this function)
    uniqSegments : (takes the return of this function)


    Examples
    --------

    >>> import numpy as np
    >>> import seg1d.algorithm as alg

    >>> # convenience function for generating wave
    >>> def s(f1, f2, f3): return np.sin( np.linspace(f1, f2, f3) )

    Define some scales that have correlations

    >>> x = { 10: s(-np.pi*1, np.pi*1, 10), 20: s(-np.pi*2, np.pi*2, 10) }

    Query the peaks in the data

    >>> np.around(alg.getPeaks(x), decimals=7)
    array([[10.       ,  0.9848078,  7.       ],
           [20.       ,  0.9848078,  1.       ],
           [20.       ,  0.8660254,  6.       ]])

    Define a minimum for the peak

    >>> np.around(alg.getPeaks(x,minC = 0.9), decimals=7)
    array([[10.       ,  0.9848078,  7.       ],
           [20.       ,  0.9848078,  1.       ]])

    '''

    #iterate through each scaled window time periods to find the peaks
    peakArr = []
    for wSize in x:
        row = x[wSize]
        #only take peaks above a height and optional distance
        peaks, _ = find_peaks(row, height=minC,distance=dst)
        #make an array of correlation,window size, index
        peakArr +=  [ [wSize,row[y],y] for y in peaks ] 

    #sort by highest correlations
    sortedPeaks = sorted(peakArr, key=itemgetter(1),reverse=True)

    return sortedPeaks


def uniqSegments(sortedPeaks,srcLen):
    '''
    Unique Segment Identification

    | Find unique segment(s) in a sequence of correlation values. 
    | Guarantees segments are not overlapping
    
    Parameters
    ----------

    sortedPeaks : n x 3 array
        n x 3 array sorted by highest to lowest correlation 
        of form ``[ scale (int), correlation(float) , peak index (int) ]``
        
    srcLen : int
        length of the target data, used to block out possible segments
        

    Returns
    -------

    n x 3 array ``[ start index, end index, correlation ]``
    None if no segments are found
    

    See Also
    --------

    getPeaks : (input for this function)
    clusterSegments : (takes in the return of this function)

    Examples
    --------

    >>> import numpy as np
    >>> import seg1d.algorithm as alg
    
    >>> p = [ [10, 0.90, 7  ],
    ...     [10, 0.89, 8  ],
    ...     [20, 0.80, 20 ],
    ...     [25, 0.70, 40 ],
    ...     ]

    >>> el = 50

    >>> alg.uniqSegments(p,el)
    [[7, 17, 0.9], [20, 40, 0.8], [40, 65, 0.7]]

    '''

    #TODO prioritize a correlation that is closer to the original reference size
    # if there are multiples

    #make an array to block out the defined segments so they don't overlap
    segmentLoc  = np.ones((srcLen))
    #empty array for segment groups to use in clustering
    segGroups   = []
    #go through the correlation list
    for peak in sortedPeaks:
        # in order of highest correlation, match it to a peak
        # find which window the peak is in
        wSize  = peak[0]
        corr   = peak[1]
        sPos   = peak[2]

        # add the window size to start indexS
        ePos   = sPos+wSize

        #if segment does not overlap
        newSeg = segmentLoc[sPos:ePos]
        # remove that size from the segment array
        if (0==newSeg).any(): continue

        # store the start and end points of the segment, with the corresponding correlation
        segGroups.append([sPos,ePos,corr])
        segmentLoc[sPos:ePos].fill(0)
    
    if len(segGroups) == 0: return None
    
    return segGroups 


def clusterSegments(segGroups,segAdder=0.5,nClust=2):
    '''
    Clustering 

    Clusters segments based on correlation values

    Parameters
    ----------
    segGroups : n x 3 array
        ``[ [ start index, end index, correlation ] ]``

    segAdder : float, optional
        0.0 to 1.0 or None
        If not None, the value that is added to the cluster groups to force
        a correlation cluster of the highest values


    Other Parameters
    ----------------

    nClust : int, optional
        number of clusters to group data in (Default 2)

        If ``nClust=0``, returns segGroups


    Returns
    -------

    n x 3 array
        ``[start segment, end segment, correlation score of segment]``
    

    Warns
    -----

    Segment Adder value was included in final cluster.This may mean cluster is poorly defined or Adder is too high.
        It is removed before being returned. However, it may be a sign of poor clustering settings as the intention
        of the segment adder is to force clustering of highly similar segments by creating
        a lower group (therefore, it should not be in the high cluster group).

    See Also
    --------

    uniqSegments : (input for this function)

    Examples
    --------

    >>> import numpy as np
    >>> import seg1d.algorithm as alg

    >>> x = [[7, 17, 0.90], [20, 40, 0.88], [40, 65, 0.8], [50, 65, 0.70]]
    >>> alg.clusterSegments(x)
    [[7, 17, 0.9], [20, 40, 0.88], [40, 65, 0.8], [50, 65, 0.7]]
    >>> alg.clusterSegments(x,segAdder=None)
    [[7, 17, 0.9], [20, 40, 0.88], [40, 65, 0.8]]
    >>> alg.clusterSegments(x,segAdder=0.85)
    [[7, 17, 0.9], [20, 40, 0.88], [40, 65, 0.8]]

    Note: This should raise the following warning:

    UserWarning: Segment Adder value was included in final cluster.This may mean cluster is poorly defined or Adder is too high.

    >>> alg.clusterSegments(x,nClust=3)
    [[7, 17, 0.9], [20, 40, 0.88], [40, 65, 0.8]]
    >>> alg.clusterSegments(x,segAdder=None,nClust=3)
    [[7, 17, 0.9], [20, 40, 0.88]]


    '''

    if nClust == 0: return segGroups

    segGroups = deepcopy(segGroups)

    #Add a correlation of the lower threshold to force a cluster of good data if necessary
    if segAdder is not None: segGroups.append([-1,-1,segAdder])

    #Check for incorrect segments by clustering
    corrVals = [x[2] for x in segGroups]

    #define the x value series
    x_grid = np.ones((len(corrVals),))
    x = list(zip(x_grid,corrVals))

    #use clustering to find the most likely reference segments
    cluster = AgglomerativeClustering(n_clusters=nClust, affinity='euclidean', linkage='single')
    cluster.fit_predict(x)

    # retrieve only highest ranked
    segClust = []
    #since correlations are sorted, first cluster label is the desired cluster
    topClust = cluster.labels_[0]  
    for i,label in enumerate(cluster.labels_):
        if label != topClust: continue
        segClust.append(segGroups[i])

    if [-1,-1,segAdder] in segClust:
        warnings.warn('Segment Adder value was included in final cluster.'
                      'This may mean cluster is poorly defined or Adder is too high.', stacklevel=2)
        segClust.remove([-1,-1,segAdder])

    return segClust


def resample(x,s):
    '''
    Interpolation

    Apply a cubic interpolation on an n x m dataset that is resampled to the number of samples

    Parameters
    ----------
    x : n x m array
        n-number of datasets with length m
        
    s : int
        number of samples to interpolate x

    Returns
    -------
    n x s array 
        interpolated dataset


    See Also
    --------

    clusterSegments : (input for this function)
    resample : (takes in the return of this function)


    Examples
    --------

    >>> import numpy as np
    >>> import seg1d.algorithm as alg

    >>> x = np.sin( np.linspace(-3, 3, 10) )
    >>> alg.resample(x,6)
    array([[-0.14112001, -0.97319156, -0.56423116,  0.56423116,  0.97319156,
             0.14112001]])
    >>> x = np.array([x,x**2])
    >>> alg.resample(x,6)
    array([[-0.14112001, -0.97319156, -0.56423116,  0.56423116,  0.97319156,
             0.14112001],
           [ 0.01991486,  0.94687756,  0.31972116,  0.31972116,  0.94687756,
             0.01991486]])

    '''
    if x.ndim == 1: x = np.array([x])

    def interSub(y):
        f = interp1d(range(y.size), y, kind='cubic')
        return f
    def getInter(y):
        p = np.linspace(0,y.size-1,num=s,endpoint=True)
        return interSub(y)( p )

    #make an empty numpty array to store reinterpolated data
    resampled = np.empty((x.shape[0],s),dtype=np.float64)    
    #store the interpolated data for each array
    for i in range(0,len(x)):
        resampled[i] = getInter(x[i])

    return resampled

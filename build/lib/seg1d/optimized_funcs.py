'''
.. module:: optimized_funcs
   :platform: Unix, Windows
   :synopsis: optimized functions.

'''

import numpy as np
import numba


@numba.jit(nopython=True,fastmath = True)
def rCor(x,Y):
    '''
    Correlation of multiple arrays to a single array using a rolling
    window correlation.

    Parameters
    ----------
    x : 1d array
        target array

    Y : ndarray
        references resampled to correct size

    Returns
    -------
    n x m array
        correlations of one ndarray to an m x ndarray


    Notes
    -----
    This will try to use numba for optimization. 


    Examples
    --------

    >>> import numpy as np
    >>> import seg1d.optimized_funcs as optF 

    >>> x = np.sin( np.linspace(-3, 3, 25) )
    >>> y = np.sin( np.linspace(-3, 3, 60) ).reshape(3,20)

    >>> optF.rCor(x,y)
    array([[-0.50743663, -0.66692675, -0.78849873, -0.87803067, -0.93682968,
            -0.96013818],
           [ 0.83362263,  0.91097751,  0.94663428,  0.94663428,  0.91097751,
             0.83362263],
           [-0.96013818, -0.93682968, -0.87803067, -0.78849873, -0.66692675,
            -0.50743663]])

    '''

    rSize, w = Y.shape # number of references , size of reference
    cSize = x.size-w+1 #size of the rolling correlation array

    #empty array for putting rolling correlation
    rCorr = np.empty((rSize,cSize)) 

    for i in range(0,rSize):
        y = Y[i]
        #get the correlation between the values
        rCorr[i] = vCor(x,y) 

    return rCorr

@numba.jit(nopython=True,fastmath = True)
def vCor(x,y):
    '''
    Rolling correlation between two arrays 
    
    Optimized by numba if available

    Parameters
    ----------
    x : 1D array
        array to use as static data

    y : 1D array
        array to use as rolling data

    Returns
    -------
    1D array
        correlations at each increment

        ``(``size = size(x) - size(y) + 1``

    Notes
    -----
    Required: ``size(x) > size(y)``


    Examples
    --------

    >>> import numpy as np
    >>> import seg1d.optimized_funcs as optF 

    >>> x = np.sin( np.linspace(-3, 3, 25) )
    >>> y = np.sin( np.linspace(-3, 3, 20) )

    >>> optF.vCor(x,y)
    array([0.83212194, 0.90933756, 0.94493014, 0.94493014, 0.90933756,
           0.83212194])

    '''

    ySize = y.size
    xSize = x.size
    corrs = np.empty(((xSize-ySize)+1,))
    n = ySize
    for i in range(0,(xSize-ySize)+1):
        X = x[i:i+ySize]
        Y = y
        xSum = 0.0
        ySum = 0.0
        for k in range(0,n):
            xSum += X[k]
            ySum += Y[k]
        xMean = xSum/n
        yMean = ySum/n
        num = 0.0
        sumx2 = 0.0
        sumy2 = 0.0
        for j in range(0,n):
            xm = (X[j] - xMean) 
            ym = (Y[j] - yMean)
            num += xm*ym
            sumx2 += xm*xm
            sumy2 += ym*ym
        denom = np.sqrt( sumx2 * sumy2 )
        corrs[i] = num/denom
    return corrs

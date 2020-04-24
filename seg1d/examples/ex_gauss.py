'''

.. plot::

    >>> import seg1d 
    >>> import numpy as np
    >>> import matplotlib.pylab as plt
    >>> import scipy.signal as signal 

    >>> # create an array of data
    >>> x = np.linspace(-1, 1, 2000)
    >>> # get an array of data from a Gaussian pulse 
    >>> targ = signal.gausspulse(x, fc=5)

    >>> # define a segment within the sine wave to use as reference
    >>> t_s,t_e    = 950,1050
    >>> # cut a segment out to use as a reference data
    >>> refData    = [ { 'gauss' : targ[t_s:t_e] } ]
    >>> targData   =   { 'gauss' : targ } 
    >>> refWeights =   { 'gauss' : 1 }

    >>> ### define some test parameters
    >>> minWin   = 98 #minimum percent to scale down reference data
    >>> maxWin   = 105 #maximum percent to scale up reference data
    >>> sizeStep = 1 #step to use for correlating reference to target data

    >>> # call the segmentation algorithm
    >>> segments = seg1d.segment_data(refData,targData,refWeights,minWin,maxWin,sizeStep)
    >>> print(np.around(segments,decimals=7))
    [[9.500000e+02 1.050000e+03 1.000000e+00]
     [7.550000e+02 8.540000e+02 9.867665e-01]
     [1.146000e+03 1.245000e+03 9.867665e-01]
     [1.343000e+03 1.441000e+03 9.498135e-01]
     [5.590000e+02 6.570000e+02 9.498135e-01]
     [1.540000e+03 1.638000e+03 8.949109e-01]
     [3.620000e+02 4.600000e+02 8.949109e-01]
     [1.738000e+03 1.836000e+03 8.301899e-01]
     [1.640000e+02 2.620000e+02 8.301899e-01]]

    >>> plt.figure(figsize=(15,4)) # doctest: +SKIP
    >>> # plot the full pulse
    >>> plt.plot(x, targ,linewidth=6,alpha=0.2,label='Target') # doctest: +SKIP
    >>> # plot the original reference segment
    >>> plt.plot(x[t_s:t_e], targ[t_s:t_e],linewidth=8,alpha=0.5,label='Reference') # doctest: +SKIP
    >>> # plot all segments found
    >>> for s,e,c in segments:
    ...     plt.plot(x[s:e], targ[s:e],dashes=[0.5,0.5],linewidth=4,alpha=0.8,label='Segments') # doctest: +SKIP
    >>> plt.legend() # doctest: +SKIP
    >>> plt.show() # doctest: +SKIP

'''

import seg1d 
import numpy as np
import matplotlib.pylab as plt
import scipy.signal as signal 

# create an array of data
x = np.linspace(-1, 1, 2000)
# get an array of data from a Gaussian pulse
targ = signal.gausspulse(x, fc=5)

# define a segment within the pulse to use as reference
t_s, t_e    = 950, 1050
# cut a segment out to use as a reference data
refData    = [{'gauss' : targ[t_s:t_e]}]
targData   =  {'gauss' : targ} 
refWeights =  {'gauss' : 1}

### define some test parameters
minWin   = 98  # minimum percent to scale down reference data
maxWin   = 105 # maximum percent to scale up reference data
sizeStep = 1   # step to use for correlating reference to target data

# call the segmentation algorithm
segments = seg1d.segment_data(refData,targData,refWeights,minWin,maxWin,sizeStep)
print(np.around(segments, decimals=7))

plt.figure(figsize=(15, 4))
# plot the full pulse
plt.plot(x, targ, linewidth=6, alpha=0.2, label='Target')
# plot the original reference segment
plt.plot(x[t_s:t_e], targ[t_s:t_e], linewidth=8, alpha=0.5, label='Reference')
# plot all segments found
for s, e, c in segments:
    plt.plot(x[s:e], targ[s:e],dashes=[0.5,0.5],linewidth=4,alpha=0.8,label='Segments')
plt.legend()
plt.show()


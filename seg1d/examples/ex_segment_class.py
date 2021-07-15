'''
    >>> import numpy as np
    >>> import seg1d 
    >>> #retrieve the sample reference, target, and weight data
    >>> r,t,w = seg1d.sampleData()
    >>> # define some test parameters
    >>> minW = 70 #minimum percent to scale down reference data
    >>> maxW = 150 #maximum percent to scale up reference data
    >>> step = 1 #step to use for correlating reference to target data
    >>> #call the segmentation algorithm
    >>> np.around(seg1d.segment_data(r,t,w,minW,maxW,step), 5)
    array([[207.      240.        0.91242]
           [342.      381.        0.88019]
           [ 72.      112.        0.87768]])
 
'''

import seg1d 

#retrieve the sample reference, target, and weight data
r,t,w = seg1d.sampleData()

### define some test parameters
minW = 70 #minimum percent to scale down reference data
maxW = 150 #maximum percent to scale up reference data
step = 1 #step to use for correlating reference to target data

#call the segmentation algorithm
segments = seg1d.segment_data(r,t,w,minW,maxW,step)

print(segments)
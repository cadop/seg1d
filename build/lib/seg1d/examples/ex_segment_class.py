'''
    >>> import seg1d 
    >>> #retrieve the sample reference, target, and weight data
    >>> r,t,w = seg1d.sampleData()
    >>> # define some test parameters
    >>> minW = 70 #minimum percent to scale down reference data
    >>> maxW = 150 #maximum percent to scale up reference data
    >>> step = 1 #step to use for correlating reference to target data
    >>> #call the segmentation algorithm
    >>> seg1d.segmentData(r,t,w,minW,maxW,step)
    [[207, 240, 0.9124223704844657], [342, 381, 0.880190111545897], [72, 112, 0.8776795468035664]]

'''

import seg1d 

#retrieve the sample reference, target, and weight data
r,t,w = seg1d.sampleData()

### define some test parameters
minW = 70 #minimum percent to scale down reference data
maxW = 150 #maximum percent to scale up reference data
step = 1 #step to use for correlating reference to target data

#call the segmentation algorithm
segments = seg1d.segmentData(r,t,w,minW,maxW,step)

print(segments)
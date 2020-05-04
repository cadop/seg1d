import seg1d
import numpy as np
import matplotlib.pylab as plt

# Data can be constructed as a numpy array

# create an array of data
x = np.linspace(-np.pi*2, np.pi*2, 2000)
# get an array of data from a sin function 
targ = np.sin(x)

# To use the basic method interface, the data must be labeled

# define a segment within the sine wave to use as reference
t_s,t_e = 200,400
# cut a segment out to use as a reference data
refData = [ { '0' : targ[t_s:t_e] } ]
targData = {'0' : targ} 
refWeights = {'0' : 1}

### define some test parameters
minWin = 98 #minimum percent to scale down reference data
maxWin = 105 #maximum percent to scale up reference data
sizeStep = 1 #step to use for correlating reference to target data

#call the segmentation algorithm
segments = seg1d.segment_data(refData,targData,refWeights,minWin,maxWin,sizeStep)
np.around(segments, decimals=7)
# array([[2.000000e+02, 4.000000e+02, 1.000000e+00],
# [1.200000e+03, 1.398000e+03, 9.999999e-01]])

# Using matplotlib we can visualize the results

plt.figure(figsize=(10,3)) #doctest: +SKIP
# plot the full sine wave
plt.plot(x, targ,linewidth=6,alpha=0.2,label='Target') #doctest: +SKIP
# plot the original reference segment
plt.plot(x[t_s:t_e], targ[t_s:t_e],linewidth=8,alpha=0.7,label='Reference') #doctest: +SKIP
# >>>
# plot all segments found
seg_num = 1
for s,e,c in segments:
    plt.plot(x[s:e], targ[s:e],dashes=[1,1],linewidth=4,alpha=0.8, #doctest: +SKIP
    label='Segment {}'.format(seg_num)) #doctest: +SKIP
    seg_num += 1 #doctest: +SKIP
plt.xlabel('Angle [rad]') #doctest: +SKIP
plt.ylabel('sin(x)') #doctest: +SKIP
plt.legend() #doctest: +SKIP
plt.tight_layout() #doctest: +SKIP
plt.show() #doctest: +SKIP

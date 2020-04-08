import seg1d
import numpy as np
import matplotlib.pylab as plt

#create an array of data
x         = np.linspace(-np.pi*2, np.pi*2, 2000)
#get an array of data from a sin function 
targ      = np.sin(x)

#make another array of sine wave data scaled larger 
x2        = np.linspace(-np.pi*1, np.pi*1, 2000)
#get an array of data from a sin function 
refSin    = np.sin(x2)

#define a segment within the sine wave to use as reference
t_s,t_e = 1000,2000
#cut a segment out to use as a reference data
refData    = [ { 'npsin' : refSin[t_s:t_e] } ]
targData   =   { 'npsin' : targ          } 
refWeights =   { 'npsin' : 1                }

### define some test parameters
minWin   = 50 #minimum percent to scale down reference data
maxWin   = 200 #maximum percent to scale up reference data
sizeStep = 1 #step to use for correlating reference to target data

#call the segmentation algorithm
segments = seg1d.segmentData(refData,targData,refWeights,minWin,maxWin,sizeStep)
print(segments)

#plot the part of the reference data 
plt.plot(x2, refSin,linewidth=8)
plt.plot(x2[1000:2000],refSin[1000:2000])
plt.show()

#plot the full sine wave
plt.plot(x, targ,linewidth=8)

#plot all segments found
for seg in segments:
    s = seg[0]
    e = seg[1]
    plt.plot(x[s:e], targ[s:e],dashes=[1,1],linewidth=6)
plt.show()
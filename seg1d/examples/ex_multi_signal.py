import seg1d 
import numpy as np
import matplotlib.pylab as plt
import scipy.signal as signal 

#create an array of data
x1 = np.linspace(-1, 1, 2000)
x = np.linspace(-1, 1, 4000)
#get an array of data from a gauss pulse and sawtooth function 
targ = signal.gausspulse(x1, fc=7)
targ = np.append(targ,signal.sawtooth(2 * np.pi * 5 * x1))

#define a segment within the sine wave to use as reference
t_s,t_e    = 950,1050
#cut a segment out to use as a reference data
refData    = [ { 'npsin' : targ[t_s:t_e] } ]
targData   =   { 'npsin' : targ          } 
refWeights =   { 'npsin' : 1                }

### define some test parameters
minWin   = 98 #minimum percent to scale down reference data
maxWin   = 105 #maximum percent to scale up reference data
sizeStep = 1 #step to use for correlating reference to target data

#call the segmentation algorithm
segments = seg1d.segment_data(refData,targData,refWeights,minWin,maxWin,sizeStep)
print(segments)

#plot the full sine wave
plt.plot(x, targ,linewidth=8,alpha=0.5,label='Target')
#plot the original reference segment
plt.plot(x[t_s:t_e], targ[t_s:t_e],linewidth=6,alpha=0.7,label='Reference')
#plot all segments found
for s,e,c in segments:
    plt.plot(x[s:e], targ[s:e],dashes=[0.5,0.5],linewidth=4,alpha=0.8,label='Segment')
plt.legend()
plt.show()


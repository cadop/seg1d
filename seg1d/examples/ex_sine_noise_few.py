import seg1d
import numpy as np
import matplotlib.pylab as plt
import seg1d.examples.noise as segnoise

#create an array of data
x = np.linspace(-np.pi*2, np.pi*2, 2000)
#get an array of data from a sin function 
targ = np.sin(x)
#add noise to the signal 
targ = segnoise.add_noise(targ,snr=40)

#Plot the target
plt.figure(figsize=(10,3)) #doctest: +SKIP
plt.plot(x, targ,linewidth=4,alpha=0.5,label='Target')#doctest: +SKIP
plt.legend()#doctest: +SKIP
plt.show()#doctest: +SKIP

#define a segment within the sine wave to use as reference
t_s,t_e = 200,400
#number of reference datasets to generate for the example

#make reference data with different random noise on a segment of the original
refData = segnoise.add_noise(np.sin(x),snr=45)[t_s:t_e] 

#Plot the reference
plt.plot(x[t_s:t_e], refData,linewidth=4,alpha=0.5,label='Reference')#doctest: +SKIP
plt.legend()#doctest: +SKIP
plt.show()#doctest: +SKIP

#Make an instance of the segmenter
s = seg1d.Segmenter()
#set scaling parameters
s.minW,s.maxW,s.step = 90, 110, 1
#Set target and reference data
s.set_target(targ)
s.add_reference(refData)
#call the segmentation algorithm
segments = s.segment()
print(segments)


plt.figure(figsize=(10,3))#doctest: +SKIP
#plot the full sine wave
plt.plot(x, targ,linewidth=4,alpha=0.2,label='Target')#doctest: +SKIP
#plot the location of the original reference segment 
# NOTE this is just the location, the actual reference data is shown above
plt.plot(x[t_s:t_e], targ[t_s:t_e],linewidth=2,alpha=0.7,label='Reference')#doctest: +SKIP
#plot all segments found
for seg in segments:
    st = seg[0]
    e = seg[1]
    plt.plot(x[st:e], targ[st:e],dashes=[1,1],linewidth=2,alpha=0.8,label='Segment')#doctest: +SKIP
plt.legend()#doctest: +SKIP
plt.show()#doctest: +SKIP

# From the plot, it is clear there is a segment that doesn't belong. 
# By accessing the Segmenter attributes, the algorithm and this error are better understood (and resolved). 

# First we look at the original segments before clustering
print(s.groups)

# It turns out these are the same number of segments as the final. 
# This happens as the clustering algorithm adds a correlation to force 2 clusters.
# This Attribute, ``Segmenter.cAdd``, defaults to 0.5. 
# In this example, that sets the correlation values to (approx.) 0.99,0.99,0.86,0.5
# Modifying this attribute would then change the clusters, for example:

s.cAdd = 0.8
print( s.segment() )

# Likewise, it is the presence of this added variable that causes the problem and removing it resolves the issue.
s.cAdd = None
print( s.segment() )

# If the target data is expected to be highly similar to the reference data, the best solution is to set ``cAdd`` to None.
# 
# Alternatively, the minimum correlation for a given segment can be set with the ``Segmenter.cMin`` attribute.
s.cMin = 0.9
print( s.segment() )

# Since the ``cAdd`` was removed, the only segments available were both 0.99, making the clustering result in a single segment. 
# If ``cAdd`` is set back to the default, the segment is correct. 
s.cAdd = 0.5
segments = s.segment() 
print(segments)


plt.figure(figsize=(10,3))#doctest: +SKIP
#plot the full sine wave
plt.plot(x, targ,linewidth=4,alpha=0.2,label='Target')#doctest: +SKIP
#plot the original reference segment
plt.plot(x[t_s:t_e], targ[t_s:t_e],linewidth=2,alpha=0.7,label='Reference')#doctest: +SKIP
#plot all segments found
for seg in segments:
    st = seg[0]
    e = seg[1]
    plt.plot(x[st:e], targ[st:e],dashes=[1,1],linewidth=2,alpha=0.8,label='Segment')#doctest: +SKIP
plt.legend()#doctest: +SKIP
plt.show()#doctest: +SKIP

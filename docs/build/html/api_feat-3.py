#Make an instance of the segmenter
s = seg1d.Segmenter()
#set scaling parameters
s.minW,s.maxW,s.step = 98, 105, 1
#Set target and reference data
s.t, s.r, s.w = t,r,w
#call the segmentation algorithm
segments = s.segment()
print(np.around(segments,decimals=7))
# [[204.        245.          0.7128945]
# [ 70.        112.          0.6670482]
# [340.        382.          0.6630886]]

plt_t = s.masked_t #get a NaN masked array of the target data

# plot masked target
plt.figure(figsize=(15,4)) # doctest: +SKIP
plt.plot(plt_t.T,alpha=0.5) # doctest: +SKIP
plt.show() # doctest: +SKIP

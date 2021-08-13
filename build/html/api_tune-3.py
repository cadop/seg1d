# To find the sub-series segment, an instance of the ``Segmenter`` class is created,
# basic scaling parameters, and the target and reference data are assigned.

# Make an instance of the segmenter
s = seg1d.Segmenter()
#set scaling parameters
s.minW,s.maxW,s.step = 90, 110, 1
#Set target and reference data
s.set_target(targ)
s.add_reference(refData)
#call the segmentation algorithm
segments = s.segment()
np.around(segments, decimals=7)
# array([[1.200000e+03, 1.420000e+03, 9.916268e-01],
# [2.000000e+02, 4.000000e+02, 9.904041e-01],
# [4.000000e+02, 5.820000e+02, 8.933443e-01],
# [1.421000e+03, 1.601000e+03, 8.833249e-01]])

# After running the segmentation algorithm, we plot the segment the reference
# data should be located, along with the segments that were found.


plt.figure(figsize=(10,3))#doctest: +SKIP
#plot the full sine wave
plt.plot(x, targ,linewidth=4,alpha=0.2,label='Target')#doctest: +SKIP
#plot the location of the original reference segment 
# NOTE this is just the location, the actual reference data is shown above
plt.plot(x[t_s:t_e], targ[t_s:t_e],linewidth=6,alpha=0.7,label='Reference')#doctest: +SKIP
#plot all segments found
seg_num = 1
for seg in segments:
    st = seg[0]
    e = seg[1]
    plt.plot(x[st:e], targ[st:e],dashes=[1,1],linewidth=2,alpha=0.8, #doctest: +SKIP
    label='Segment {}'.format(seg_num)) #doctest: +SKIP
    seg_num += 1
plt.xlabel('Angle [rad]')#doctest: +SKIP
plt.ylabel('sin(x)')#doctest: +SKIP
plt.legend()#doctest: +SKIP
plt.tight_layout()#doctest: +SKIP
plt.show()#doctest: +SKIP

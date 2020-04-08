# From the plot, it is clear there are segments that do not belong.
# By accessing the ``Segmenter`` attributes, the algorithm and this error are better understood (and resolved).

# First we look at the original segments before clustering
np.around(S.groups, decimals=7)
# array([[1.200000e+03, 1.420000e+03, 9.916268e-01],
# [2.000000e+02, 4.000000e+02, 9.904041e-01],
# [4.000000e+02, 5.820000e+02, 8.933443e-01],
# [1.421000e+03, 1.601000e+03, 8.833249e-01],
# [5.830000e+02, 7.650000e+02, 7.286635e-01],
# [1.602000e+03, 1.782000e+03, 6.541974e-01]])

# As shown in the output, there are a total of 6 segments found before clustering.

# As the distribution of segments is apporx. [0.99,0.99,0.89,0.88,0.72,0.65],
# the attribute, ``Segmenter.cAdd``, (defaults to 0.5) that is added for forcing clusters
# only combines the last two values, 0.72 and 0.65 in the lower cluser.

# Modifying this attribute would then change the clusters, for example:

S.cAdd = 0.8
np.around(S.segment(), decimals=7)
# array([[1.200000e+03, 1.420000e+03, 9.916268e-01],
# [2.000000e+02, 4.000000e+02, 9.904041e-01]])


# If the attribute is removed, then only the original segments are used in the clustering.
# However, this results in the same cluster as the original where the default of ``cAdd`` was 0.5.

S.cAdd = None
np.around(S.segment(), decimals=7)
# array([[1.200000e+03, 1.420000e+03, 9.916268e-01],
# [2.000000e+02, 4.000000e+02, 9.904041e-01],
# [4.000000e+02, 5.820000e+02, 8.933443e-01],
# [1.421000e+03, 1.601000e+03, 8.833249e-01]])

# Alternatively, the minimum correlation for a given segment can be set with the ``Segmenter.cMin`` attribute.

S.cMin = 0.9
np.around(S.segment(),decimals=7)
# array([[1.200000e+03, 1.420000e+03, 9.916268e-01]])


# Since the ``cAdd`` was removed, the only segments available (higher than 0.9 correlation)
# were both 0.99, making the clustering result in a single segment.

# If ``cAdd`` is set back to the default, the segment is correct.

S.cAdd = 0.5
segments = S.segment() 
np.around(segments, decimals=7)
# array([[1.200000e+03, 1.420000e+03, 9.916268e-01],
# [2.000000e+02, 4.000000e+02, 9.904041e-01]])

# Finally, plotting these segments shows the alignment and logical sub-series
# identification.

plt.figure(figsize=(10,3))#doctest: +SKIP
#plot the full sine wave
plt.plot(x, targ,linewidth=4,alpha=0.2,label='Target')#doctest: +SKIP
#plot the original reference segment
plt.plot(x[t_s:t_e], targ[t_s:t_e],linewidth=6,alpha=0.7,label='Reference')#doctest: +SKIP
#plot all segments found
for seg in segments:
    s = seg[0]
    e = seg[1]
    plt.plot(x[s:e], targ[s:e],dashes=[1,1],linewidth=2,alpha=0.8,label='Segment')#doctest: +SKIP
plt.legend()#doctest: +SKIP
plt.show()#doctest: +SKIP

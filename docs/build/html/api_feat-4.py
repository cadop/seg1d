# To use a subset of the features, the weights can be redefined,
# which may result in a different segmentation result

sub = [('C7','z'),('T10','z'),('CLAV','z')]
s.w = { x: w[x] for x in sub }
segments = s.segment()

print(np.around(segments,decimals=7))
# [[  2.         44.          0.9648465]
# [341.        383.          0.9646419]
# [203.        244.          0.9644605]
# [273.        314.          0.9640178]
# [ 72.        113.          0.9632458]
# [139.        180.          0.9624551]]

plt_t = s.t_masked #get a NaN masked array of the target data

# plot masked target
plt.figure(figsize=(15,4)) # doctest: +SKIP
plt.plot(plt_t.T,alpha=0.5) # doctest: +SKIP
plt.show() # doctest: +SKIP

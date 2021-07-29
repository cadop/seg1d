s.set_target(target)

s.w = weight_dict
segments = s.segment()
print(np.around(sorted(segments, key=lambda x: x[0])[:3], decimals=5))
# [[ 42.       67.        0.99856]
# [112.      137.        0.99864]
# [181.      208.        0.99709]]

# Now that we have segmented the data, the masked array can be plotted to show the results.

plt_t = s.t_masked #get a NaN masked array of the target data
# plot masked target
plt.figure(figsize=(15,4))  # doctest: +SKIP
plt.plot(plt_t.T,alpha=0.5)  # doctest: +SKIP
plt.show()  # doctest: +SKIP

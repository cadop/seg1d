# Match feature length and center time series

# The first function we use for pre-processing the data is `match_len`.
# This will take the largest array of all reference datasets and rescale the other datasets
# to this longer size

ref_data = proc.Features.match_len(raw_r)

# We can now plot the length-matched datasets to see how the reference segments do show
# similarity over the same scaled timespan

plt_r = np.asarray( [ x for y in ref_data for x in y.values()  ]  ).T
plt.figure(figsize=(3,3))  # doctest: +SKIP
plt.plot(plt_r,alpha=0.3)  # doctest: +SKIP
plt.show()  # doctest: +SKIP

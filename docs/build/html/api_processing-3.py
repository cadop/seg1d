# This next process is not always necessary, but is convenient to know. It simply shifts the mean
# of each array in the references to center along the 0 axis.

ref_data = proc.Features.center(ref_data)

# Make sure all reference data has valid keys
# In this step, we use the `shared` function by passing all the datasets we will will use
# to ensure no feature keys are missing. This requires a dictionary to map each feature correctly

ref_data, tar_data = proc.Features.shared(ref_data, raw_t)

# Generate weights from the segmented data
# One of the most important steps for many use cases is the automatic weighting of multiple features.
# The `gen_weights` function takes a list of reference datasets and finds the features that match
# best among all of the references.  It then normalizes all the results from 0 to 1.
# This is important to note, as it means some features will not be used.
# If all of your features are necessary or should be used, this function should be skipped.

weights = proc.Features.gen_weights(ref_data)

# Finally, the last step of pre-processing is to get which params to use and limit to specific ones.
# In this example, we take only the top 20 features, limit to the normalized score of 0.8, and pass
# an empty list, which means we use all available features.  If there was a list of features
# that you wanted to include, passing this key list of strings would be possible.

weight_dict = proc.Features.meaningful(weights, limit=0.8, top=20, include_keys=[])

# Now we can take a look at the reference data that we will use for segmentation.
# This data has also been centered (a few steps before)

plt_r = np.asarray( [ x for y in ref_data for x in y.values()  ]  ).T
plt.figure(figsize=(3,3))  # doctest: +SKIP
plt.plot(plt_r,alpha=0.3)  # doctest: +SKIP
plt.show()  # doctest: +SKIP

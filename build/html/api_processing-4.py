# ########################## SEG1D Analysis #######################

# At this point the data is properly processed and features weighted.
# From here on, the normal segmentation process (as seen in the other examples) is applied.

s = seg1d.Segmenter()
s.minW, s.maxW, s.step = 70, 150, 1

for r in ref_data: 
    s.add_reference(r)

# As this sample dataset has multiple targets, we will just use the first one.
# However, you could iterate over all the target trials by wrapping the remaining code
# under this example loop:
# for idx, target in enumerate(tar_data):

# Run the analysis on the first target data.

target = tar_data[0]

# We can visualize this target data before segmentation

plt_t = np.asarray( [ x for x in target.values() ] )
plt.figure(figsize=(15,4))  # doctest: +SKIP
plt.plot(plt_t.T,alpha=0.5)  # doctest: +SKIP
plt.show()  # doctest: +SKIP

# The final segments are shown by calling the property ``masked_t`` which returns the
# target data as an ndarray with NaN values for areas not found to be segments.


plt.figure(figsize=(15,3))  # doctest: +SKIP
plt.plot(S.masked_t.T)  # doctest: +SKIP
plt.show()  # doctest: +SKIP

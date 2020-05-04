# The final segments are shown by calling the property ``t_masked`` which returns the
# target data as an ndarray with NaN values for areas not found to be segments.


plt.figure(figsize=(15,3))  # doctest: +SKIP
plt.plot(s.t_masked.T)  # doctest: +SKIP
plt.show()  # doctest: +SKIP

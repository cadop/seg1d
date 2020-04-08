# plot target data
plt_t = np.asarray( [ x for x in t.values() ] )
plt.figure(figsize=(15,4)) # doctest: +SKIP
plt.plot(plt_t.T,alpha=0.5) # doctest: +SKIP
plt.show() # doctest: +SKIP

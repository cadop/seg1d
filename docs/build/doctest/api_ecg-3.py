#use only 1 reference
S.clearReference()
S.addReference( ecg[927:1057] )

refs = S.r
refs = np.asarray( [ x[y] for x in refs for y in x ] )

plt.figure(figsize=(5,3))  # doctest: +SKIP
plt.plot(refs.T)  # doctest: +SKIP
plt.show()  # doctest: +SKIP

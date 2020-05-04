#use only 1 reference
s.clear_reference()
s.add_reference( ecg[927:1057] )

refs = s.r
refs = np.asarray( [ x[y] for x in refs for y in x ] )

plt.figure(figsize=(5,3))  # doctest: +SKIP
plt.plot(refs.T)  # doctest: +SKIP
plt.xlabel("time in s")  # doctest: +SKIP
plt.ylabel("ECG in mV")  # doctest: +SKIP
plt.tight_layout()  # doctest: +SKIP
plt.show()  # doctest: +SKIP

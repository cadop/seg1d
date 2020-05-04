#remove first part of data (contains reference)
s.set_target(ecg[1500:3500])
s.nC = 2
s.cMin = 0.7

segments = s.segment()

print(np.around(segments,decimals=7))
# [[7.350000e+02 8.540000e+02 9.462850e-01]
# [1.093000e+03 1.213000e+03 9.242974e-01]
# [9.140000e+02 1.046000e+03 9.059727e-01]
# [3.620000e+02 4.980000e+02 9.009127e-01]
# [5.470000e+02 6.800000e+02 8.940106e-01]
# [1.262000e+03 1.390000e+03 8.868629e-01]
# [1.776000e+03 1.902000e+03 8.771139e-01]
# [1.609000e+03 1.729000e+03 8.689476e-01]
# [1.440000e+03 1.559000e+03 8.646669e-01]
# [1.730000e+02 3.060000e+02 8.029426e-01]]

res = s.t_masked

plt.figure(figsize=(15,3))  # doctest: +SKIP
plt.plot(res.T)  # doctest: +SKIP
plt.xlabel("time in s")  # doctest: +SKIP
plt.ylabel("ECG in mV")  # doctest: +SKIP
plt.tight_layout()  # doctest: +SKIP
plt.show()  # doctest: +SKIP

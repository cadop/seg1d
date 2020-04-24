import random
import numpy as np
from scipy.misc import electrocardiogram
import matplotlib.pyplot as plt
import seg1d 

# After imports, the scipy signal ECG data is called and some segments are taken.

ecg = electrocardiogram() #get the scipy sample data 
ref_slices = [[927, 1057],[1111, 1229]] #pick sample endpoints

s = seg1d.Segmenter()  #create the segmenter

refs = [ ecg[x[0]:x[1]] for x in ref_slices ]
for r in refs: s.add_reference(r) #set reference data

s.set_target(ecg[1500:3500]) #set the target data to the ecg after ref
segments = s.segment()  # run segmenter with defaults

print(np.around(segments,decimals=7))
# [[1.607000e+03 1.729000e+03 8.169533e-01]
# [7.380000e+02 8.220000e+02 8.123868e-01]
# [9.190000e+02 1.003000e+03 8.120505e-01]
# [1.439000e+03 1.552000e+03 8.092366e-01]
# [3.600000e+02 4.930000e+02 8.077664e-01]
# [1.091000e+03 1.213000e+03 8.043364e-01]
# [1.775000e+03 1.895000e+03 7.998723e-01]
# [1.720000e+02 3.000000e+02 7.926582e-01]
# [1.268000e+03 1.340000e+03 7.847107e-01]
# [5.540000e+02 6.280000e+02 7.802931e-01]]

# The reference data is automatically scaled to the largest reference in the dataset
# when the ``segment`` method is called. Therefore, by retrieving this attribute
# we can plot what the reference set looks like when the lengths are normalized.

# In the example, it is clear the peaks of the reference segments are not aligned.
# This discrepency, due to the averaging of all reference data items, will be seen
# in the final segments of the target data later.

refs = s.r
refs = np.asarray( [ x[y] for x in refs for y in x ] )

plt.figure(figsize=(5,3))  # doctest: +SKIP
plt.plot(refs.T)  # doctest: +SKIP
plt.show()  # doctest: +SKIP

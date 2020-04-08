import numpy as np
import matplotlib.pylab as plt
import seg1d 

#retrieve the sample reference, target, and weight data
r,t,w = seg1d.sampleData(c=0.5)

# Note: The reference data shown here is centered at 0 on the y axis (vertical).
# As the algorithm process is based on the shape of the curve, it is irrelevant
# what this offset is.

# plot reference data
plt_r = np.asarray( [ x for y in r for x in y.values()  ]  ).T
plt.figure(figsize=(3,3)) # doctest: +SKIP
plt.plot(plt_r,alpha=0.3) # doctest: +SKIP
plt.show() # doctest: +SKIP

# First we import ``seg1d``, a helper function for adding noise in the example called
# ``segnoise``, and the plotting utils from ``matplotlib``.

import seg1d
import numpy as np
import matplotlib.pylab as plt
import seg1d.examples.noise as segnoise

# Next an array of data is generated and a sine wave is created.
# A signal-noise ratio of 30 is added to the sine wave.

# create an array of data
x = np.linspace(-np.pi*2, np.pi*2, 2000)
# get an array of data from a sin function 
targ = np.sin(x)
# add noise to the signal 
np.random.seed(123)
targ = segnoise.add_noise(targ,snr=30)

# The target data that is used for finding segments in looks like:

# Plot the target
plt.figure(figsize=(10,3)) #doctest: +SKIP
plt.plot(x, targ,linewidth=4,alpha=0.5,label='Target')#doctest: +SKIP
plt.legend()#doctest: +SKIP
plt.show()#doctest: +SKIP

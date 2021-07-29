# First we import numpy and matplotlib (to plot for the example)

import numpy as np
import matplotlib.pyplot as plt

# Then import the base seg1d and the seg1d processing module

import seg1d
import seg1d.processing as proc

# ##########################  SEG1D Processing #######################

# To start, we load an array of dictionaries provided as sample data in seg1d.
# raw_r is the set of references, and raw_t is a set of targets

raw_r, raw_t = seg1d.sample_input_data()

# First we can take a look at the reference datasets, noticing they are all different lengths

plt.figure(figsize=(3,3))  # doctest: +SKIP
for r in raw_r:
    plt_r = np.asarray( [ x for x in r.values()  ]  ).T
    plt.plot(plt_r,alpha=0.3)  # doctest: +SKIP
plt.show()  # doctest: +SKIP

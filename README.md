# seg1d

Segmentation of one-dimensional data. 


## Overview

seg1d is an open-source python package for the automated segmentation and extraction of time series data using one or more reference sequences. The segmentation process allows users to apply various methods and parameters for the process through weighted reference features in a rolling correlation size-varying window. Correlations can be averaged across the references and a peak detection algorithm finds individual segments. Non-overlapping segments are identified and a clustering algorithm groups the most similar subsequence movements within the target. The package was developed for movement sciences but should be useful to anyone interested in extracting correlated subsequences from a dataset. 

![seg1d](docs/build/plot_directive/api_basic-1.png)


### Documentation

Full Documentation Available Online: https://cadop.github.io/seg1d/


### Alternatives

There are existing libraries that provide clustering and similarity measures for querying subseries data. 

  * https://www.cs.ucr.edu/~eamonn/UCRsuite.html (UCR Suite, "Ultrafast subsequence search under both Dynamic Time Warping (DTW) and Euclidean Distance (ED)"
  * https://github.com/rtavenar/tslearn (tslearn, "Machine learning tools for the analysis of time series")


## Quickstart 


### Dependencies

Currently tested on ``Python 3.8`` on Ubuntu 18.04 and Windows 10. 

Required Packages:

``numpy>=1.18``, ``scipy>=1.4.1``, ``sklearn>=0.22``, ``numba>=0.48``

For documentation:

``sphinx>=2``

### Installation

```pip install seg1d```


### Example usage

The documentation contains examples using data of both generated data (e.g., sine wave) and real-world examples (i.e., motion capture data). 

To quickly get started, try importing the seg1d module and using the provided sample data. 

```python

import seg1d 

#retrieve the sample reference, target, and weight data
r,t,w = seg1d.sampleData()
# define scaling percentage and rolling step size
minW, maxW, step  = 70, 150, 1 
#call the segmentation algorithm
seg1d.segmentData(r,t,w,minW,maxW,step)

# Should output an array equal to:
# array([[207.       , 240.       ,   0.9124224],
#        [342.       , 381.       ,   0.8801901],
#        [ 72.       , 112.       ,   0.8776795]])

```

For more examples, please refer to the full documention. 

## Project Info

This project was used for the following paper: 

(Under Review) Schwartz, Mathew; Pataky, Todd; Sui Geok Karen, CHUA; Wei Tech, ANG; and Donnelly, Cyril (2019) "AUTOMATED MULTI-FEATURE SEGMENTATION OF TREADMILL RUNNING," ISBS Proceedings Archive: Vol. 37 : Iss. 2 , Article 1. 

### Community

Issues and feature requests should be submitted on [github](https://github.com/cadop/segment1d/issues). 

Please check the Community Guidelines for further details on contributing. 


### Credits

Code written and developed by Mathew Schwartz (New Jersey Institute of Technology).

Data used in sample provided by Precision Rehab, Rehabilitation Research Institute of Singapore.

Project was funded in part by the Agency for Science, Technology and Research (A\*STAR), Nanyang Technological University (NTU) and the National Health Group (NHG) (RRG3: 2019/19002).

### License

Please refer to the full [LICENSE](https://github.com/cadop/segment1d/blob/master/LICENSE.txt).
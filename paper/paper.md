---
title: 'seg1d: A Python package for Automated segmentation of one-dimensional (1D) data'
tags:
  - Python
  - biomechanics
  - data series
  - movement
  - motion capture
authors:
  - name: Mathew Schwartz
    orcid: 0000-0003-3662-7203
    affiliation: 1
  - name: Todd C. Pataky
    orcid: 0000-0002-8292-7189
    affiliation: 2
  - name: Cyril J. Donnelly
    affiliation: 3
affiliations:
 - name: New Jersey Institute of Technology
   index: 1
 - name: Kyoto University, Department of Human Health Sciences
   index: 2
 - name: Nanyang Technological University, Rehabilitation Research Institute of Singapore
   index: 3
date: 25 March 2020
bibliography: paper.bib

---

# Summary

The term segmentation refers to the division of a data series into segments. In this paper, segments refer to a contiguous time series which is a subset of another time series [@bouchard2006automated]. Identifying these segments requires a reference series to be found in the larger series, which can be an exact copy or an approximation. When an approximation of the desired segment is used, the metric and method for identifying similarity of all subsets is essential to achieving a desired result. Additionally, multiple references may be desired to further describe the aspects of segment similarity, some of which may be more important than others. 

Segmenting human motion is a topic studied in various fields such as robotics (e.g., humanoids), biomechanics, and computer graphics (e.g., gaming and animation). In the human movement sciences, segmentation is often performed as the labeling of specific events, such as the components of a gait cycle, for analysis and interpretation of the data within these labeled bounds. Subjectively defining what is a movement or a phase of a movement can be particularly difficult due to variations in what one may define as a single movement. As such, the points at which the movement or phases of a movement starts and ends can be ambiguous. The averaging of multiple features (e.g., marker trajectories, joint angles, or other information derived from the data) of a movement or even multiple movements (e.g., multiple marker trajectories from multiple observation sets) allows for a tolerance to some individual features failing to provide an expected characteristic (e.g., a signal above or below a threshold value from a force plate) that may normally be relied upon for identifying an event. Defining weights of individual features, with either algorithmic approaches or through expert knowledge, further facilitates segmentation of similar movements. 

With feature-rich data such as multiple marker trajectories from motion capture, the reduction of meaningful features is important for segmentation performance [@bouchard2015segmenting]. The use of marker trajectory and ground reaction force, without computing kinematics, has been shown to be sufficient in movement segmentation tasks [@lin2016comparison]. Unique feature creation, extraction, and storage can be used to additionally index databases for fast movement-based time-series data retrieval [@kapadia2013efficient]. Subseries searching of databases has often been performed with similarity metrics, each with their own individual downfalls, e.g.: Longest Common Subseries (LCSS), Euclidean Distance (ED), and Dynamic Time Warping (DTW) [@vlachos2003indexing]. Discrete Fourier Transformation (DFT) has also been used as a method for improving the efficiency of windowed correleations [@zhu2002statstream]. Data reduction techniques for optimization can also be used in windowed correlations of generic time-series data [@cole2005fast].

Peak detection has been used to identify gait events through the inference of a cyclic motion and reducing reliance on physical meanings of the signal by searching for the assumed cyclic pattern rather than a given threshold value or calculated joint angle [@jiang2017robust]. Peak detection from cross-correlated data has been used for gait event detection in accelerometry data [@yoneyama2013accelerometry]. Alternative methods for segmenting data have used physical devices to act as switches on foot contact [@agostini2013segmentation]. Most recently, deep neural networks have been used to predict foot contact, but requires a large amount (i.e., thousands of trials) of training data [@kidzinski2019automatic]. Using DTW, [@sarsfield2019segmentation] was able to identify movements in realtime with a single reference segment. Allowing both single and multiple reference segments, as well as multiple features and optional weights, the segmentation of various data is more practical in a single package.  

[//]: # Segmentation of movement data, when automated, is often built with specific features such as velocity of a marker or kinematic data in software such as Visual3D. 


# Statement of Need

Subsequence identification and similarity between a reference(s) and target data items is a commonly desired task done both manually and automatically in a variety of fields. The ability to further automate and create reliable, consistent results, is of importance for many data processing related tasks. For example, in typical motion capture sessions of walking gait in a lab, embedded force plates provide high fidelity measurements for foot-strike and toe-off. However the cycles before and after this event are often discarded. By using a collection of features from a known segment (i.e., the cycle over the force-plate), similar sequences within a trial can be found and used for study. Furthermore, some movements are not so well defined with these external sensing tools, and rather a template movement selected by a human is the most reasonable way to identify the sequence of data describing a particular motion. 

seg1d is an open-source Python package for the automated segmentation and extraction of time series data using one or more reference sequences. The segmentation process allows users to apply various methods and parameters for the process through weighted reference features in a rolling correlation size-varying window of any scale below the length of the targeted data. Correlations can be averaged across the references and a peak detection algorithm finds individual segments. Non-overlapping segments are identified and a clustering algorithm groups the most similar subsequence movements within the target. The package was developed for movement sciences but can be useful to anyone interested in extracting correlated subsequences from a dataset. 

![Sample segments in a timeseries from a reference \label{fig:example}](api_basic-1.png)


# Acknowledgements

This work was supported in part by the Agency for Science, Technology and Research (A\*STAR), Nanyang Technological University (NTU) and the National Health Group (NHG) (RRG3: 2019/19002).

Todd Pataky is supported through the Kiban B Grant 17H02151 (Japan Society for the Promotion of Science).

# References

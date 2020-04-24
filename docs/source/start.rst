===============
Getting Started
===============

In this section, a few simple examples are given to ensure the installation is working
and you are able to segment data.  These examples call a method provided that uses
default parameters for the algorithms within the segmentation process but contains
the data related parameters such as scaling and step size for the matching process. 


Sample Data
===========

A basic example of checking the installation using the included sample data.

.. automodule:: seg1d.examples.ex_simple
	:members:
	

Sine Wave
=========

.. automodule:: seg1d.examples.ex_sine
	:members:
	
Gauss
=====

In this example a Gaussian pulse is used to show segmentation on the varying shape of different amplitude. 
As the center arc is given as reference, the multiple extending arcs are found as well. Through 
the output of the segments, the correlation values can be seen to decrease, although still
clustered within the group. 

.. automodule:: seg1d.examples.ex_gauss
	:members:
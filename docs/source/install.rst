============
Installation
============

Check dependencies
------------------
Currently tested on ``Python 3.8+``.

For the package: ``numpy>=1.18``, ``scipy>=1.4.1``, ``sklearn>=0.22``, ``numba>=0.48``

For building documentation: ``sphinx``, ``scipy`` html_theme

Get seg1d
-------------

``pip install seg1d``

Building Documentation
----------------------

Documentation is built using sphinx with the scipy html_theme in the `docs` folder. 

``make clean``

``make html``


Testing
--------

Docstrings examples should be compliant with ``doctest``. 
Navigate to the `docs` folder and run:

``make doctest``

A summary report will be generated and should not have any failed conditions. 
Note, this should be done after building the documentation with ``make html``.

Due to variations in OS, many of the doctests use ``np.around`` to ensure matching. 
However, sorting of correlation values is dependent on a few platform variables, 
so tests that output multiple array values that are identical may show as failed. 
The documentation is always tested on Windows 10, Python 3.8 for ensuring compliance. 
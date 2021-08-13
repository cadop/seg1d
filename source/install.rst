============
Installation
============

Check dependencies
------------------
Currently tested on ``Python 3.8+``.

For the package: ``numpy>=1.15``, ``scipy>=1.0.0``, ``sklearn>=0.2``, ``numba>=0.40``

For building documentation: ``sphinx``, ``scipy`` html_theme, ``numpydoc``, ``matplotlib``

Get seg1d
-------------

``pip install seg1d``

Building Documentation
----------------------

Documentation is built using sphinx with the scipy html_theme in the `docs` folder. 

To get the requirements for building documentation you can run:

``pip install sphinx numpydoc matplotlib``

If you have not installed ``seg1d`` you can then run the following to get the remaining requirements

``pip install numpy scipy sklearn numba``

Finally, the following two lines will build the documentation. 

``make clean``

``make html``


Testing
--------

Docstrings examples should be compliant with ``doctest``. 
Navigate to the `docs` folder and run:

``make doctest``

A summary report will be generated and should not have any failed conditions. 
Note, this should be done after building the documentation with ``make html``.

End-users can test the installation with a similar method provided through the
examples. 

After installation, start a python interactive console and import:

``from seg1d.examples import test``

Then run the tests with:

``test.run()``

A series of tests will be performed to check for intended output. 
While ``matplotlib`` is not a required dependency, if it is not installed, some
of the tests will fail. This will be obvious as the test will show in the 
traceback that it failed due to ``No module named 'matplotlib'``. 

Due to variations in OS, many of the doctests use ``np.around`` to ensure matching. 
However, sorting of correlation values is dependent on a few platform variables, 
so tests that output multiple array values that are identical may show as failed. 
The documentation is always tested on Windows 10, Python 3.8 for ensuring compliance. 

import sys
sys.path.append('./seg1d')
from _about import __version__
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seg1d", 
    version= __version__,
    author="Mathew Schwartz",
    author_email="umcadop@gmail.com",
    description="Automated one-dimensional subsequence segmentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cadop/seg1d",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy>=1.15','scipy>=1.0.0','scikit-learn>=0.2','numba>=0.40.0'],
    package_data={
        "": ["examples/data/*.npy"],
    },
    include_package_data=True,   
)

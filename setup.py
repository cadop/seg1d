import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seg1d", 
    version="0.0.1",
    author="Mathew Schwartz",
    author_email="cadop@umich.edu",
    description="Automated subsequence segmentation of 1-dimensional data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cadop/seg1d",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License",
        "Operating System :: Unix, Windows",
    ],
    python_requires='>=3.8',
)
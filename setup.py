from setuptools import find_packages, setup

VERSION = "0.0.1"

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="burrowts",
    version=VERSION,
    description="Simple plug and play timeseries database for storing and retreiving time-stamped values",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yusuf",
    author_email="contact@yusuf.im",
    url="https://github.com/iunary/burrowts",
    license="MIT",
    install_requires=[],
    keywords=[
        "timeseries",
        "stime-stamped",
        "timeseries store",
        "time series",
        "thread-safe",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "metatune",
    version = "0.0.1",
    author = "<AUTHOR NAME>",
    author_email = "<AUTHOR EMAIL>",
    description = "Simultaneous model selection and hyperparameter tuning of scikit-learn supervised learning algorithms with optuna implemented metaheuristic search algorithms.",
    license = "Apache License 2.0",
    keywords = "scikit-learn optuna automl",
    url = "https://github.com/ches-001/metatune",
    packages=['metatune', 'tests'],
    long_description=read('readme.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Natural Language :: English",
    ],
)

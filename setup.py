#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


CLASSIFIERS = """
Development Status :: 4 - Beta
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries
"""


setup(
    name="Kumiko",
    version="0.1",
    py_modules=["kumikolib"],
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["opencv-python>=4.2.0.32"],
    # metadata to display on PyPI
    author="nicoo",
    description="set of tools to compute useful information "
    "about comic book pages, panels, and more",
    keywords="comic panel cutter opencv",
    url="https://github.com/njean42/kumiko",  # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/njean42/kumiko/issues",
        "Documentation": "https://github.com/njean42/kumiko",
        "Source Code": "https://github.com/njean42/kumiko",
    },
    classifiers=CLASSIFIERS.strip().split(),
    # could also include long_description, download_url, etc.
    long_description=long_description,
    long_description_content_type="text/markdown",  # Optional (see note above)
    extras_require={  # Optional
        "test": ["pytest", "pytest-flake8", "pytest-black"],
    },
)

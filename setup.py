#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name="django-data-importer",
    version="0.1.0-p1",
    description="",
    author="Felipe 'chronos' Prenholato",
    author_email="philipe.rp@gmail.com",
    url="http://github.com/chronossc/django-data-importer",
    packages = find_packages(exclude=('sampleprojet',)),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[
        "Django >= 1.3.4",
        "openpyxl",
        "xlrd"
    ],
    zip_safe = False,
)

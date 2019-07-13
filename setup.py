#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='imagepypelines_builtin',
      packages=find_packages(),
      entry_points={'imagepypelines.plugins': 'builtin = imagepypelines_builtin'}
      )

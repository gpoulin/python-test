#!/usr/bin/env python3
from distutils.core import setup, Extension
import numpy.distutils.misc_util
import sys
import os
import glob

extC = Extension(
                "_pure_c", ["pure_c.c"],
                include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs()
                )





setup(ext_modules = [extC],
)

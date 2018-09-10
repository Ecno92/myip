#!/usr/bin/env python3
import os
import sys

from setuptools import setup

CURDIR = os.path.realpath(os.path.join(os.path.dirname(
    sys.modules['__main__'].__file__)))
sys.path.insert(0, os.path.join(CURDIR, 'src'))

if __name__ == '__main__':
    setup()

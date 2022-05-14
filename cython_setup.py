import os
from setuptools import find_packages
from distutils.core import setup
from Cython.Build import cythonize


def find_pyx(path='.'):
    pyx_files = []
    for root, dirs, filenames in os.walk(path):
        for fname in filenames:
            if fname.endswith('.pyx'):
                pyx_files.append(os.path.join(root, fname))
    return pyx_files


setup(ext_modules=cythonize(find_pyx(),
      language_level=3),
      packages=find_packages())

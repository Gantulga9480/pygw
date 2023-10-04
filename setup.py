import os
from setuptools import setup, find_packages
from Cython.Build import cythonize
import numpy as np


def find_pyx(path='.'):
    pyx_files = []
    for root, dirs, filenames in os.walk(path):
        for fname in filenames:
            if fname.endswith('.pyx'):
                pyx_files.append(os.path.join(root, fname))
    return pyx_files


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PyGameWizard",
    version="2.0.0-beta",
    author="Gantulga G",
    author_email="limited.tulgaa@gmail.com>",
    description="Pygame base class for ease of use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gantulga9480/PyGameWizard",
    packages=find_packages(),
    license='MIT',
    install_requires=['pygame', 'Cython', 'numpy'],
    ext_modules=cythonize(find_pyx(),
                          language_level=3,
                          annotate=True),
    include_dirs=[np.get_include()],
    package_data={'': ['*.pyi']}
)

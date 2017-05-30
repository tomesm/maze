from setuptools import setup
from Cython.Build import cythonize
import numpy
import glob

setup(
    name='maze',
    ext_modules=cythonize(glob.glob('maze/*.pyx'), language_level=3, include_dirs=[numpy.get_include()]),
    include_dirs=[numpy.get_include()],
    install_requires=[
        'Cython',
        'NumPy',
    ],
)

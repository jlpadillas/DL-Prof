from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize([
    Extension("queue", ["papi.pyx"],
              libraries=["papi"])
    ])
)
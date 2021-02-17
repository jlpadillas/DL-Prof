from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name='Hello world app',
    ext_modules=cythonize([
        Extension("hello", ["hello.pyx"],
                  libraries=["/home/jlpadillas01/papi/src/libpapi.so"])
    ]),
    zip_safe=False,
)

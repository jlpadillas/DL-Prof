#! /usr/bin/env python3
# -- coding: utf-8 --

# standard library
import ctypes
from ctypes import *
# import pathlib

# 3rd party packages
import numpy as np

# ------------------------------------------------------------------------ #
# Multiplicacion de dos matrices: A = M  N usando numpy

__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["Universidad de Cantabria"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"


if __name__ == "__main__":
    # Load the shared library into ctypes
    # libname = pathlib.Path().absolute() / "libpapi.so.6.0"

    libname = "/home/jlpadillas01/TFG/bin/my_papi.so"
    p_lib = CDLL(libname)

    print(type(p_lib))

    # print("PAPI_is_initialized() = ", p_lib.PAPI_is_initialized())

    dim_x = 500
    dim_y = dim_x

    # Genera las matrices random
    # M = np.random.rand(dim_x, dim_y)
    # N = np.random.rand(dim_x, dim_y)

    # Genera las matrices "controladas"
    M = np.empty([dim_x, dim_y], dtype=float)
    N = np.empty([dim_x, dim_y], dtype=float)
    # M, N = np.mgrid[0.0:dim_x,0.0:dim_y]

    # ROI
    # ----------------------------------------
    # EventSet = p_lib.PAPI_num_components()
    # print("PAPI_num_components() = ", EventSet)

    # A = np.matmul(M, N)

    # ----------------------------------------
    # print(M)
    # print(N)
    # print(A)

#! /usr/bin/env python3
# -- coding: utf-8 --

# standard library
import sys
import ctypes
from ctypes import *
import pathlib

# 3rd party packages
import numpy as np

# local source
from my_papi import my_papi

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

    # -------------------------------------------------------------------- #
    # Params
    # -------------------------------------------------------------------- #
    # Current working directory (Makefile from)
    PWD = pathlib.Path(__file__).parent.parent.absolute()
    # Carpeta donde se encuentran los ejecutables
    BIN_DIR = PWD / "bin"
    # Carpeta donde se encuentran las librerias generadas
    LIB_DIR = PWD / "lib"
    # Carpeta donde se vuelcan los datos de salida
    OUT_DIR = PWD / "out"
    # Carpeta donde se encuentran los archivos fuente
    SRC_DIR = PWD / "src"

    # Hay que hacer append del path del src para que encuentre ficheros
    sys.path.append(SRC_DIR)

    # Se crea un objeto de la clase my_papi
    libname = LIB_DIR / "libmy_papi.so"
    mp = my_papi(libname)

    # -------------------------------------------------------------------- #
    # Execution
    # -------------------------------------------------------------------- #

    # casa = mp.malloc(10)

    # print(casa)

    # mp.free(casa)

    # print(casa)

    # mp.start_measure()

    # mp.stop_measure()


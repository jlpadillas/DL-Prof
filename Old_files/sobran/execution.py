#! /usr/bin/env python3
# -- coding: utf-8 --

# ------------------------------------------------------------------------ #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["University of Cantabria"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
if __name__ == "__main__":
    """Dependiendo del valor pasado por parametro, se ejecuta la multipli-
    cacion de dos matrices rellenadas con la funcion empty() o zeros(),
    ambas pertenecientes a la liberia Numpy.
    @param option variable que se pasa por parametro y que indica si se ha
        de rellenar las matrices con la funcion empty() o zeros().
    """

    # standard library
    import locale
    import os
    import pathlib
    import subprocess
    from subprocess import run
    # 3rd party packages

    # local source


    # Define the locale format
    locale.setlocale(locale.LC_ALL, '')

    # -------------------------------------------------------------------- #
    # Params
    # -------------------------------------------------------------------- #
    # Current working directory
    PWD = pathlib.Path(__file__).parent.parent.absolute()
    # Carpeta donde se encuentran los ejecutables
    BIN_DIR = PWD / "bin"
    # Carpeta donde se encuentran las librerias generadas
    LIB_DIR = PWD / "lib"
    # Carpeta donde se vuelcan los datos de salida
    OUT_DIR = PWD / "out"
    # Carpeta donde se encuentran los archivos fuente
    SRC_DIR = PWD / "src"


    M_TYPE = ["SEQ"]
    M_SIZE = [512]
    M_MULT = ["MULTITHREAD"]

    RAW = True

    # -------------------------------------------------------------------- #
    # Compile
    # -------------------------------------------------------------------- #
    command = ["make", "-C", PWD, "test_compile"]
    run(command, stdout=subprocess.DEVNULL)  # , stderr=subprocess.STDOUT)

    # -------------------------------------------------------------------- #
    # Execution
    # -------------------------------------------------------------------- #
    for m_type in M_TYPE:
        for m_size in M_SIZE:
            for m_mul in M_MULT:
                
                print(m_type, m_size, m_mul)


# ------------------------------------------------------------------------ #

def format():
    pass


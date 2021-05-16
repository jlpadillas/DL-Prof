#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["Universidad de Cantabria", "Pablo Abad", "Pablo Prieto"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# --------------------------------------------------------------------------- #

if __name__ == "__main__":

    # standard library
    import os
    import pathlib
    import sys

    # Forces the program to execute on CPU
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

    # Just disables the warning, doesn't take advantage of AVX/FMA to run faster
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # -------------------------------------------------------------------- #
    # Params
    # -------------------------------------------------------------------- #
    # Current working directory (Makefile from)
    PWD = pathlib.Path(__file__).parent.parent.absolute()

    # Carpeta donde se encuentran los ejecutables
    BIN_DIR = PWD / "bin"
    # Carpeta donde se encuentran los archivos de configuracion
    CFG_DIR = PWD / "conf"
    # Carpeta donde se encuentran las librerias generadas
    LIB_DIR = PWD / "lib"
    # Carpeta donde se vuelcan los datos de salida
    OUT_DIR = PWD / "out"
    # Carpeta donde se encuentran los archivos fuente
    SRC_DIR = PWD / "src"

    # Adding path to my_papi lib (path_to_import from TFG folder)
    path_to_import = PWD.parent.parent.absolute() / "mat_mul/Python/src"
    sys.path.insert(0, str(path_to_import))
    # -------------------------------------------------------------------- #

    # 3rd party packages

    # local source
    from MyPapiResults import MyResults

    # -------------------------------------------------------------------- #

    # Creates a object
    fm = MyResults()

    # ! main_papi.py
    csv_file = "out/main_papi.csv"
    html_file = "out/main_papi.html"
    # fm.create_plotly_table(csv_file, html_file)
    fm.create_dash_table(csv_file)

    # ! main_callback_batch.py
    csv_file = "out/main_callback_batch.csv"
    html_file = "out/main_callback_batch.html"
    # fm.create_plotly_table(csv_file, html_file)
    # fm.create_dash_table(csv_file)

    # ! main_callback_epoch.py
    csv_file = "out/main_callback_epoch.csv"
    html_file = "out/main_callback_epoch.html"
    # fm.create_plotly_table(csv_file, html_file)
    # fm.create_dash_table(csv_file)

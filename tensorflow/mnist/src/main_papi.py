#!/usr/bin/env python3
# coding: utf-8

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
    """
    TODO
    """

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

    # Adding path to Python files (path_to_import from TFG folder)
    path_to_import = PWD.parent.parent.absolute() / "mat_mul/Python/src"
    sys.path.insert(0, str(path_to_import))
    # -------------------------------------------------------------------- #

    # 3rd party packages

    # local source
    from my_papi import my_papi
    from mnist import mnist

    # -------------------------------------------------------------------- #

    # Se crea un objeto de la clase my_papi
    libname = LIB_DIR / "libmy_papi.so"
    mp = my_papi(libname)

    # Create an object mnist
    mnst = mnist()

    mnst.setup()

    # mnst.set_parallelism(None, None)

    # -------------------------------------------------------------------- #
    # MY_PAPI
    # -------------------------------------------------------------------- #
    # events_file = CFG_DIR / "events_pc.cfg"
    # events_file = CFG_DIR / "events_laptop.cfg"
    # events_file = CFG_DIR / "events_node.cfg"
    events_file = CFG_DIR / "events_node_mnist.cfg"
    # -------------------------------------------------------------------- #

    mp.prepare_measure(str(events_file), cpus=None)

    mp.start_measure()

    # -------------------------------------------------------------------- #
    # ROI
    # -------------------------------------------------------------------- #

    mnst.fit()

    # -------------------------------------------------------------------- #
    # END ROI
    # -------------------------------------------------------------------- #

    mp.stop_measure()

    csv_file = "out/main_file.csv"
    html_file = "out/main_file.html"
    # mp.print_measure(csv_file)
    mp.print_measure()

    mp.finalize_measure()

    # fm = format_results()
    # fm.create_plotly_table(csv_file, html_file)

    # mp.check_results(output_file)

    # mp.create_dash_table(output_file)

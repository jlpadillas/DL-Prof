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

    # Define the locale format
    locale.setlocale(locale.LC_ALL, '')

    # -------------------------------------------------------------------- #
    # Loads the my_papi library
    # -------------------------------------------------------------------- #
    import sys
    import pathlib

    # Absolute path to this script
    MY_PAPI_DIR = pathlib.Path(__file__).absolute()
    # Now, we have to move to the root of this workspace ([prev. path]/TFG)
    MY_PAPI_DIR = MY_PAPI_DIR.parent.parent.parent.parent.parent.absolute()
    # From the root (TFG/) access to my_papi dir. and its content
    MY_PAPI_DIR = MY_PAPI_DIR / "my_papi"
    # Folder where the configuration files are located
    CFG_DIR = MY_PAPI_DIR / "conf"
    # Folder where the library is located
    LIB_DIR = MY_PAPI_DIR / "lib"
    # Folder where the source codes are located
    SRC_DIR = MY_PAPI_DIR / "src"

    # Add the source path and import the library
    sys.path.insert(0, str(SRC_DIR))
    from MyPapi import *

    # -------------------------------------------------------------------- #
    # Params for the measure
    # -------------------------------------------------------------------- #
    # Path to the library, needed to create an object of class my_papi
    libname = LIB_DIR / "libmy_papi.so"

    # Load a file with the events
    # events_file = CFG_DIR / "events_pc.cfg"
    # events_file = CFG_DIR / "events_laptop.cfg"
    events_file = CFG_DIR / "events_node.cfg"

    # Measures on all cpus
    cpus = None

    # Output file with the measures
    # output_file = "out/main_papi_results.csv"
    # output_file = None
    # -------------------------------------------------------------------- #


    # ! main_papi.py
    csv_file = "out/mnist_papi.csv"
    html_file = "out/mnist_papi.html"
    # fm.create_plotly_table(csv_file, html_file)
    MyPapi.create_dash_table(csv_file)

    # ! main_callback_batch.py
    # csv_file = "out/mnist_callback_batch.csv"
    # html_file = "out/main_callback_batch.html"
    # fm.create_plotly_table(csv_file, html_file)
    # fm.create_dash_table(csv_file)
    # MyPapi.dash_table_by_cpus_static(csv_file)


    # ! main_callback_epoch.py
    # csv_file = "out/main_callback_epoch.csv"
    # html_file = "out/main_callback_epoch.html"
    # # fm.create_plotly_table(csv_file, html_file)
    # # fm.create_dash_table(csv_file)
    # MyPapi.dash_table_by_cpus_static(csv_file)

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
    # import sys
    import locale

    # 3rd party packages

    # local source
    from matrix import matrix

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
    output_file = "out/main_papi_results.csv"
    # output_file = None
    # -------------------------------------------------------------------- #

    # Now, we can create a object of my_papi and setup the config.
    mp = MyPapi(libname)
    mp.prepare_measure(str(events_file), cpus)

    # Creates an object of matrix class
    mat = matrix()

    # Reads the parameters
    if len(sys.argv) != 3:
        print("[ERROR] Wrong parameters.\n\tUsage: python3 main.py "
              "[MATRIX_TYPE] [MATRIX_SIZE]")
        raise mat.Error

    mat_type = sys.argv[1]
    dim_x_and_y = int(sys.argv[2])

    # We will use square matrices
    dim_x = dim_x_and_y
    dim_y = dim_x_and_y

    # Populates the matrices
    if mat_type == "EMPTY":
        M = mat.init_empty(rows=dim_x, cols=dim_y)
        N = mat.init_empty(rows=dim_x, cols=dim_y)
    elif mat_type == "RAND":
        M = mat.init_rand(rows=dim_x, cols=dim_y)
        N = mat.init_rand(rows=dim_x, cols=dim_y)
    elif mat_type == "SEQ":
        M = mat.init_seq(rows=dim_x, cols=dim_y)
        N = mat.init_seq(rows=dim_x, cols=dim_y)
    elif mat_type == "ZEROS":
        M = mat.init_zeros(rows=dim_x, cols=dim_y)
        N = mat.init_zeros(rows=dim_x, cols=dim_y)
    else:
        print("[ERROR] Unknown parameter '{}'. Run the program with "
              "argument 'EMPTY', 'RAND', 'ZEROS' or 'SEQ'.".format(mat_type))
        raise mat.Error

    # ROI -> Se multiplican
    mp.start_measure()

    mat.mat_mul(M, N)

    mp.stop_measure()
    mp.print_measure(output_file)
    mp.finalize_measure()

    # Prints the results
    # MyPapi.sum_events(events_file, output_file)
    # mp.check_results(events_file, output_file)
    # ! Caution! file "output_file" may be overwritted if executed this script
    # ! more than one time

    if dim_x == dim_y:
        num = (dim_x * dim_x) * (2 * dim_x - 1)
        print("\n FP operations expected (aprox.): " +
              locale.format_string('%.0f', num, grouping=True))

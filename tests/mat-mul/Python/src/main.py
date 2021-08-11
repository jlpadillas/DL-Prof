#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["University of Cantabria", "Pablo Abad", "Pablo Prieto"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    """Dependiendo del valor pasado por parametro, se ejecuta la multipli-
    cacion de dos matrices rellenadas con la funcion empty() o zeros(),
    ambas pertenecientes a la liberia Numpy.
    @param option variable que se pasa por parametro y que indica si se ha
        de rellenar las matrices con la funcion empty() o zeros().
    """

    # standard library
    import sys

    # 3rd party packages
    from matrix import *

    # local source

    # ----------------------------------------------------------------------- #

    MAX_MATRIX_SIZE = 100_000
    events_file = "../../../my_papi/conf/events_matmul.cfg"

    # Reads the parameters and check the correctness
    if len(sys.argv) < 4:
        print("[ERROR] Wrong parameters.\n\tUsage: python3 main.py "
              "[MATRIX_TYPE] [MATRIX_SIZE] [MULTIPLICATION TYPE]")
        sys.exit(-1)

    mat_type = sys.argv[1]
    if mat_type != "RAND" and mat_type != "SEQ":
        print("[ERROR] Wrong matrix type: %s.\n", mat_type)
        sys.exit(-1)

    dim_x_and_y = int(sys.argv[2])
    if dim_x_and_y < 0 or dim_x_and_y > MAX_MATRIX_SIZE:
        print("[ERROR] Matrix size out of bounds [0-%d].\n", MAX_MATRIX_SIZE)
        sys.exit(-1)
    rows_a = dim_x_and_y
    cols_a = dim_x_and_y
    rows_b = dim_x_and_y
    cols_b = dim_x_and_y

    mul_type = sys.argv[3]
    if mul_type != "MULTITHREAD" and mul_type != "NORMAL" and mul_type != "TRANSPOSE":
        print("[ERROR] Wrong multiplication type: %s.\n", mul_type)
        sys.exit(-1)

    # Create an object of the class matrix
    m = matrix()

    # Populate the matrices
    if mat_type == "RAND":
        M_a = m.init_rand(rows=rows_a, cols=cols_a)
        M_b = m.init_rand(rows=rows_b, cols=cols_b)
    elif mat_type == "SEQ":
        M_a = m.init_seq(rows=rows_a, cols=cols_a)
        M_b = m.init_seq(rows=rows_a, cols=cols_a)

    # ----------------------------------------------------------------------- #
    # Loads the my_papi library
    # ----------------------------------------------------------------------- #
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
    from MyPapi import MyPapi

    # ----------------------------------------------------------------------- #
    # Params for the measure
    # ----------------------------------------------------------------------- #
    # Path to the library, needed to create an object of class my_papi
    libname = LIB_DIR / "libmy_papi.so"

    # Load a file with the events
    events_file = CFG_DIR / "events_node_matmul.cfg"

    # Measures on all cpus
    # cpus = None
    # ! modify this to get the num of cpus automatic
    cpus = list(range(2, 32))

    # Output file with the measures
    csv_file = None
    if len(sys.argv) == 5:
        csv_file = sys.argv[4]

    # Now, we can create a object of my_papi and setup the config.
    mp = MyPapi(libname)
    mp.prepare_measure(str(events_file), cpus)
    # ----------------------------------------------------------------------- #

    mp.start_measure()
    # -------------------------- Region of Interest ------------------------- #
    if mul_type == "MULTITHREAD":
        M_c = m.mat_mul_multithread(M_a, M_b)
    elif mul_type == "NORMAL":
        M_c = m.mat_mul(M_a, M_b)
    elif mul_type == "TRANSPOSE":
        M_c = m.mat_mul_transpose(M_a, M_b)
    # ------------------------ END Region of Interest ----------------------- #
    mp.stop_measure()
    mp.print_measure(csv_file)
    mp.finalize_measure()

#! /usr/bin/env python3
# -- coding: utf-8 --

# standard library
import sys

# 3rd party packages

# local source
sys.path.append("/home/jlpadillas01/TFG/1.mat_mul/src/")
from matrix import matrix
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
# ------------------------------------------------------------------------ #

if __name__ == "__main__":
    """Dependiendo del valor pasado por parametro, se ejecuta la multipli-
    cacion de dos matrices rellenadas con la funcion empty() o zeros(),
    ambas pertenecientes a la liberia Numpy.
    @param option variable que se pasa por parametro y que indica si se ha
        de rellenar las matrices con la funcion empty() o zeros().
    """

    # TODO: Asignar una opción para generar las matrices
    if len(sys.argv) > 1:
        option = sys.argv[1]

    # Se usan matrices cuadradas para facilitar el calculo de operaciones.
    dim_x = 1000
    dim_y = dim_x

    # Se crea el objeto
    mat = matrix(dim_x, dim_y)

    # Se generan las dos matrices
    if option == "empty":
        mat.init_empty()
    elif option == "zeros":
        mat.init_zeros()
    else:
        print("ERROR: Wrong generation of matrices. Run the program with "
              "argument 'empty' or 'zeros'.")
        raise mat.Error

    # Se crea un objeto de la clase my_papi
    libname = "/home/jlpadillas01/TFG/2.compilation/lib/libmy_papi.so"
    mp = my_papi(libname)

    # -----------------------------------------------------
    # Ejecucion
    # -----------------------------------------------------

    # Se crea una lista con los eventos a medir

    # // Portatil
    events = [
        "fp_arith_inst_retired.128b_packed_double",
        # "fp_arith_inst_retired.128b_packed_single", # Suele ser 0
        "fp_arith_inst_retired.256b_packed_double",
        # "fp_arith_inst_retired.256b_packed_single", # Suele ser 0
        "fp_arith_inst_retired.scalar_double",
        # "fp_arith_inst_retired.scalar_single", # Suele ser 0
        # "fp_assist.any", # Suele ser 0
        "cycles",
        "instructions",
    ]

    # // PC
    # events = [
    #     # "fp_assist.any",
    #     # "fp_assist.simd_input",
    #     # "fp_assist.simd_output",
    #     # "fp_assist.x87_input",
    #     # "fp_assist.x87_output",
    #     # "fp_comp_ops_exe.sse_packed_double",
    #     # "fp_comp_ops_exe.sse_packed_single",
    #     "fp_comp_ops_exe.sse_scalar_double",
    #     # "fp_comp_ops_exe.sse_scalar_single", # no encuentra el evento!!!!!
    #     # "fp_comp_ops_exe.x87",
    #     "simd_fp_256.packed_double",
    #     "simd_fp_256.packed_single",
    #     "cycles",
    #     "instructions"
    # ]

    # -----------------------------------------------------
    # ROI
    # -----------------------------------------------------
    mp.start_measure(events)

    mat.mat_mul()

    mp.stop_measure()
    # -----------------------------------------------------
    # END ROI
    # -----------------------------------------------------

    mp.print_results()

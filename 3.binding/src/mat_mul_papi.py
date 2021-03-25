#! /usr/bin/env python3
# -- coding: utf-8 --

# standard library
import sys
import ctypes
from ctypes import *
# import pathlib

# 3rd party packages
import numpy as np

# local source
from system_setup import system_setup
sys.path.append("/home/jlpadillas01/TFG/1.mat_mul/src/")
from matrix import matrix

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

    # Se crea un objeto de para modificar la configuración del sistema
    setup = system_setup()

    # TODO: Asignar una opción para generar las matrices
    option = "zeros"
    # if len(sys.argv) > 1:
    #     option = sys.argv[1]

    # Se usan matrices cuadradas para facilitar el calculo de operaciones.
    dim_x = 5000
    dim_y = dim_x

    # Se crea el objeto
    mat = matrix(dim_x, dim_y)
    # mat = matrix()

    # Se generan las dos matrices
    if option == "empty":
        mat.empty_matrices()
    elif option == "zeros":
        mat.zeros_matrices()
    else:
        print("ERROR: Wrong generation of matrices. Run the program with "
              "argument 'empty' or 'zeros'.")
        raise mat.Error

    # Load the shared library into ctypes
    # libname = pathlib.Path().absolute() / "libpapi.so.6.0"
    libname = "/home/jlpadillas01/TFG/2.compilation/lib/libmy_papi.so"
    p_lib = CDLL(libname)

    # TODO: Hay que cambiar el path para que se pueda encontrar el .so
    # export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.:/usr/local/lib
    # TODO: Hay que habilitar la lectura de los eventos bajando el nivel de seg.
    # sudo sysctl -w kernel.perf_event_paranoid=1

    # print(type(p_lib))
    # print("PAPI_is_initialized() = ", p_lib.PAPI_is_initialized())

    # ROI
    # # ----------------------------------------
    # ptr_EventSet = ctypes.pointer(ctypes.c_int())
    # values = ctypes.c_longlong

    # # 1.
    # p_lib.my_PAPI_library_init()
    # # 2.
    # p_lib.my_PAPI_create_eventset(ptr_EventSet)
    # # 3.
    # # p_lib.my_PAPI_add_named_event(ptr_EventSet, "SIMD_FP_256:PACKED_DOUBLE")
    # # p_lib.my_PAPI_add_named_event(ptr_EventSet, "FP_COMP_OPS_EXE:SSE_SCALAR_DOUBLE")
    # # 4.
    # p_lib.my_PAPI_start(ptr_EventSet)

    # # ---------------------
    # # ROI -> Se multiplican
    # mat.multiply()
    # # ---------------------

    # # 5.
    # p_lib.stop(ptr_EventSet, values)
    # # 6.
    # p_lib.my_PAPI_shutdown()

    # print(values)

    # -----------------------------------------------------
    # Ejecucion con una unica medida
    # -----------------------------------------------------

    # Se crea una lista con los eventos a medir
    events = [
        "cycles",
        "instructions",
        # "fp_arith_inst_retired.128b_packed_double",
        # "fp_arith_inst_retired.128b_packed_single",
        "fp_arith_inst_retired.256b_packed_double",
        "fp_arith_inst_retired.256b_packed_single",
        # "fp_arith_inst_retired.scalar_double",
        # "fp_arith_inst_retired.scalar_single"
        # "fp_assist.any"
    ]

    events_bytes = []
    for i in range(len(events)):
        events_bytes.append(bytes(events[i], 'utf-8'))

    events_array = (ctypes.c_char_p * (len(events_bytes)+1))()

    events_array[:-1] = events_bytes

    # event = ctypes.c_char_p('CYCLES'.encode('ascii'))
    # print(event.value)

    # Es necesario reducir el nivel de perf para medir
    setup.set_perf_event_paranoid(1)

    # Empieza la medida de los eventos
    ptr_EventSet = p_lib.my_start_events(events_array, len(events))

    # ROI
    mat.multiply()

    # Finaliza la medida de los eventos
    values = p_lib.my_stop_events(ptr_EventSet, len(events))

    # Se sube el nivel de perf al que tenia por defecto
    setup.set_perf_event_paranoid()

    # Se imprime el valor medido
    print(values)

    # g = (ctypes.c_char*40000).from_address(values)


    # -----------------------------------------------------

    # -----------------------------------------------------
    # Ejecucion con dos medidas
    # -----------------------------------------------------

    # # Se crea una lista con los eventos a medir
    # events = ['CYCLES', 'INSTRUCTIONS']

    # b = ctypes.create_string_buffer("HEllo", 7)

    # print(ctypes.sizeof(b))

    # print(b.value)

    # # --- Lo de abajo no deberia verlo el usuario.

    # # Se cambia el formato para que pueda ser leido en C
    # # param = []
    # # for e in events:
    # #     param.append(c_char_p(e.encode('ascii')))

    # param = (ctypes.c_char_p * len(events))(*events)

    # # Es necesario reducir el nivel de perf para medir
    # setup.set_perf_event_paranoid(1)

    # # Empieza la medida de los eventos
    # ptr_EventSet = p_lib.my_start_events(param, len(param))

    # # ROI
    # mat.multiply()

    # # Finaliza la medida de los eventos
    # values = p_lib.my_stop_events(ptr_EventSet, len(param))

    # # Se sube el nivel de perf al que tenia por defecto
    # setup.set_perf_event_paranoid()

    # # Se imprime el valor medido
    # print(values)

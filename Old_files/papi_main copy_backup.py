#! /usr/bin/env python3
# -- coding: utf-8 --

# standard library
import sys
# import pathlib

# 3rd party packages
import numpy as np
import ctypes
from ctypes import *

# local source
sys.path.append("/home/jlpadillas01/TFG/mnist/src/")
sys.path.append("/home/jlpadillas01/TFG/mat_mul/src/")
from system_setup import system_setup
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
    dim_x = 3000
    dim_y = dim_x

    # Se crea el objeto
    mat = matrix()

    # Se generan las dos matrices
    if option == "empty":
        mat.init_empty()
    elif option == "zeros":
        mat.init_zeros()
    else:
        print("ERROR: Wrong generation of matrices. Run the program with "
              "argument 'empty' or 'zeros'.")
        raise mat.Error

    # Load the shared library into ctypes
    libname = "/home/jlpadillas01/TFG/mat_mul/lib/libmy_papi.so"
    p_lib = CDLL(libname)

    # TODO: Hay que cambiar el path para que se pueda encontrar el .so
    # export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.:/usr/local/lib
    # TODO: Hay que habilitar la lectura de los eventos bajando el nivel de seg.
    # sudo sysctl -w kernel.perf_event_paranoid=1

    # -----------------------------------------------------
    # Ejecucion con una unica medida
    # -----------------------------------------------------

    # Se crea una lista con los eventos a medir
    # events = [
    #     "cycles",
    #     "instructions",
    #     # "fp_arith_inst_retired.128b_packed_double",
    #     # "fp_arith_inst_retired.128b_packed_single",
    #     "fp_arith_inst_retired.256b_packed_double",
    #     "fp_arith_inst_retired.256b_packed_single",
    #     # "fp_arith_inst_retired.scalar_double",
    #     # "fp_arith_inst_retired.scalar_single"
    #     # "fp_assist.any"
    # ]

    # // PC
    # const char *events[] = [
    events = [
        "cycles",
        "instructions",
        # # "fp_assist.any",
        # # "fp_assist.simd_input",
        # # "fp_assist.simd_output",
        # # "fp_assist.x87_input",
        # # "fp_assist.x87_output",
        # # "fp_comp_ops_exe.sse_packed_double",
        # # "fp_comp_ops_exe.sse_packed_single",
        # "fp_comp_ops_exe.sse_scalar_double",
        # # "fp_comp_ops_exe.sse_scalar_single", # no encuentra el evento!!!!!
        # # "fp_comp_ops_exe.x87",
        # "simd_fp_256.packed_double",
        # "simd_fp_256.packed_single"
    ]

    # Se tiene que pasar a bytes para poder enviarlo a la funcion en C
    events_bytes = []
    for i in range(len(events)):
        events_bytes.append(bytes(events[i], 'utf-8'))

    # Se crea un array con los eventos a pasar
    events_array = (c_char_p * (len(events_bytes) + 1))()

    # Corta el string para eliminar el last char = \n
    events_array[:-1] = events_bytes


    # Es necesario reducir el nivel de perf para poder medir
    # setup.set_perf_event_paranoid(1)

    print(len(events), len(events_array))

    # Empieza la medida de los eventos
    ptr = c_int()
    p_lib.my_start_events(len(events), events_array, byref(ptr), 1)

    quit()


    # ROI
    mat.mat_mul()

    # Finaliza la medida de los eventos
    my_stop_events = p_lib.my_stop_events
    # longlongArrayType = c_longlong * len(events)
    my_stop_events.argtypes = [c_int, c_int]
    # my_stop_events.restype = longlongArrayType
    # values = p_lib.my_stop_events(ptr_EventSet, len(events))
    # my_stop_events.restype = c_char_p   # c_char_p is a pointer to a string
    # my_stop_events.restype = c_longlong * len(events)
    my_stop_events.restype = POINTER(c_longlong) * len(events)

    # pyArray = longlongArrayType()
    # print(list(pyArray))
    # pyArray = my_stop_events(ptr_EventSet, len(events))

    # print(repr(my_stop_events(ptr_EventSet, len(events))))

    # Se sube el nivel de perf al que tenia por defecto
    setup.set_perf_event_paranoid()
    # casa = (list(pyArray))
    # print(casa)
    # for i in casa:
    #     print(int(i))
    # Se imprime el valor medido
    # for i in range(0, len(events)):
    #     # print(i.value, end=" ")
    #     print(result[i])
    # print(len(result))
    # print(repr(result))

    # for i in range(len(events)):
    #     print(ctypes.cast(pyArray[i], ctypes.c_ulong))

    result = my_stop_events(ptr_EventSet, len(events))
    for i in range(0, len(events)):
        # ctypes.cast(result[i], ctypes.c_longlong)
        print((result[i].contents).value)
    
    # result.contents

    # ord(d)

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


    # ----------------- sobra?
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

    # event = ctypes.c_char_p('CYCLES'.encode('ascii'))
    # print(event.value)

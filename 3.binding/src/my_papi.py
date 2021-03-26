#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
import subprocess
from subprocess import run

# 3rd party packages
import ctypes
from ctypes import *


# local source
from system_setup import system_setup

__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["Universidad de Cantabria", "Pablo Abad"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"


class my_papi(system_setup):
    """Permite hacer cambios relativos al PC en el que se ejecuta."""

    # Attributes
    # self.cores = [] # Array de cores logicos pertenecientes al mismo fisico
    # self.p_lib = CDLL # Con el se puede acceder a la liberia y sus func.
    # self. ptr_EventSet # Puntero que indica la loc. en mem. del eventSet

    def __init__(self, path):
        """Constructor de la clase my_papi que pide por parametro la localizacion
        de la liberia libmy_papi.so."""
        super(my_papi, self).__init__()
        self.__set_my_lib(path)
    # ------------------------------------------------------------------------ #

    def __set_my_lib(self, libname):
        """Carga la libreria de libmy_papi.so, para ello es necesario indicar su
        PATH."""
        # Load the shared library into ctypes
        self.p_lib = CDLL(libname)

    def start_measure(self, events=None):
        # if events is None or isinstance(events, list):
        #     # TODO: indicar con un warning el fallo
        #     events = ["CYCLES", "INSTRUCTIONS"]  # Default measures

        # Se guarda como un atributo de la clase
        self.events = events

        # Se convierte a bytes para pasarlo a la funcion en C
        events_bytes = []
        for i in range(len(events)):
            events_bytes.append(bytes(events[i], 'utf-8'))

        # Se crea un array con los eventos a pasar
        events_array = (c_char_p * (len(events_bytes) + 1))()

        # Corta el string para eliminar el last char = \n
        events_array[:-1] = events_bytes

        # Es necesario reducir el nivel de perf para poder medir
        self.set_perf_event_paranoid(1)

        # Empieza la medida de los eventos
        self.ptr_EventSet = self.p_lib.my_start_events(
            events_array, len(events))

    def stop_measure(self):
        """Detiene la lectura de datos y devuelve un array con los valores
        medidos."""

        # Tengo que hacer espacio en memoria para traer los resultados
        # resultado = c_longlong * len(self.events)

        # Se definen los parametros de entrada y salida de la funcion C
        self.p_lib.my_stop_events.argtypes = c_int, c_int, POINTER(c_longlong)
        self.p_lib.my_stop_events.restype = c_int

        # Se inicializa
        p = (c_longlong * len(self.events))()

        self.p_lib.my_stop_events(self.ptr_EventSet, len(self.events), p)

        return list(p)
        # return resultado

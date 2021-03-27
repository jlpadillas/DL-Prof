#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
import locale
import warnings

# 3rd party packages
from ctypes import *


# local source
from system_setup import system_setup

# ------------------------------------------------------------------------ #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["Universidad de Cantabria", "Pablo Abad"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #


class my_papi(system_setup):
    """Permite realizar medidas de los eventos mediante el uso de la 
    libreria libmy_papi.so, que a su vez se basa en el codigo de PAPI."""

    # Attributes
    # ----------
    # self.cores = [] # Array de cores logicos pertenecientes al mismo fisico
    default_events = ["cycles", "instructions"]
    # self.p_lib = CDLL # Con el se puede acceder a la liberia y sus func.
    # self. ptr_EventSet # Puntero que indica la loc. en mem. del eventSet
    # self.events = [] # Eventos a ser medidos
    # selg.values = [] # lista con los valores medidos

    def __init__(self, path):
        """Constructor de la clase my_papi que recibe por parametro la 
        localizacion de la liberia libmy_papi.so."""

        super(my_papi, self).__init__()

        # Loads the library path
        self.__set_my_lib(path)

    # -------------------------------------------------------------------- #

    def start_measure(self, events=None):
        """Gets the events to be measured and starts it."""

        # If none events is passed, it just measured the default events.
        if events is None:
            warnings.formatwarning = self.__warning_on_one_line
            warnings.warn(
                "No input events, measuring default events!", Warning)
            self.events = self.default_events
        else:
            # Se guarda como un atributo de la clase
            self.events = events

        # Se convierte a bytes para pasarlo a la funcion en C
        events_bytes = []
        for i in range(len(self.events)):
            events_bytes.append(bytes(self.events[i], 'utf-8'))

        # Se crea un array con los eventos a pasar
        events_array = (c_char_p * (len(events_bytes) + 1))()

        # Corta el string para eliminar el last char = \n
        events_array[:-1] = events_bytes

        # Es necesario reducir el nivel de perf para poder medir
        self.set_perf_event_paranoid(1)

        # Empieza la medida de los eventos
        self.ptr_EventSet = self.p_lib.my_start_events(
            events_array, len(self.events))
    # -------------------------------------------------------------------- #

    def stop_measure(self):
        """Detiene la lectura de datos y guarda los valores obtenidos."""

        # Se definen los parametros de entrada y salida de la funcion C
        self.p_lib.my_stop_events.argtypes = c_int, c_int, POINTER(c_longlong)
        self.p_lib.my_stop_events.restype = c_int

        # Se guarda espacio en memoria y se leen los resultados
        self.values = (c_longlong * len(self.events))()
        self.p_lib.my_stop_events(
            self.ptr_EventSet, len(self.events), self.values)

        self.set_perf_event_paranoid()  # Default perf

    # -------------------------------------------------------------------- #

    def get_results(self, format=dict):
        """
        Return the results in a specific format.
            @param: format dict or list
            @return string with the results
        """

        # Check if the results are formated
        try:
            self.values_list and self.values_dict
        except AttributeError:
            self.__format_values()

        # Returns the value
        if format is dict:
            return self.values_dict
        elif format is list:
            return self.values_list
    # -------------------------------------------------------------------- #

    def print_results(self, format=dict):
        """
        Print the results in a specific format.
            @param: format dict or list
            @return string with the results
        """

        # Check if the results are formated
        try:
            self.values_list and self.values_dict
        except AttributeError:
            self.__format_values()

        # Sets the locale for prints
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

        # Printing with a specific format
        if format is dict:
            # Header
            print("{:>20}\t\t{:<}".format('Value', 'Event'))
            for event, value in self.values_dict.items():
                # Items
                print("{:>20_}\t\t{:<}".format(value, event).replace('_', '.'))
                # print("{:>20}\t\t{:<}".format(
                #     locale.format_string('%.0f', value, grouping=True), event))

        elif format is list:
            print(*self.values_list, sep="\t")
            # for v in self.values_list:
            #     print("{:>20}".format(locale.format_string('%.0f', v, grouping=True)))

    # -------------------------------------------------------------------- #

    def __format_values(self):
        """Transform the results obtanied as an array and as a dictionary"""

        # Check if the measure has been done/finished
        try:
            self.values
        except AttributeError:
            raise self.NoMeasureFinishedError

        # List
        self.values_list = list(self.values)

        # Dictionary
        self.values_dict = {}
        for i in range(len(self.events)):
            self.values_dict[self.events[i]] = self.values[i]
    # -------------------------------------------------------------------- #

    def __set_my_lib(self, libname):
        """Carga la libreria de libmy_papi.so, para ello es necesario 
        indicar su PATH."""

        # Load the shared library into ctypes
        self.p_lib = CDLL(libname)
    # -------------------------------------------------------------------- #

    def __warning_on_one_line(self, message, category, filename, lineno,
                              file=None, line=None):
        """Format the warning output."""

        return '%s:%s:\n\t%s: %s\n' % (filename, lineno, category.__name__,
                                       message)
    # -------------------------------------------------------------------- #

    # -------------------------------------------------------------------- #
    # define Python user-defined exceptions

    class Error(Exception):
        """Base class for other exceptions"""
        pass

    class NoMeasureFinishedError(Error):
        """Raised when there is no result obtnaied."""
        pass
    # -------------------------------------------------------------------- #
# ------------------------------------------------------------------------ #

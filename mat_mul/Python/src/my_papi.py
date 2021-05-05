#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
import locale
import warnings

# 3rd party packages
from ctypes import *

# local source
from system_setup import system_setup

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


class my_papi(system_setup):
    """Permite realizar medidas de los eventos mediante el uso de la 
    libreria libmy_papi.so, que a su vez se basa en el codigo de PAPI."""

    # Attributes
    # ----------
    # self.cores = [] # Array de cores logicos pertenecientes al mismo fisico
    # self.p_lib = CDLL # Con el se puede acceder a la liberia y sus func.
    # self.events = []  # Eventos a ser medidos
    # selg.values = []  # lista con los valores medidos

    # self. ptr_EventSets # Puntero que indica la loc. en mem. del eventSet

    def __init__(self, path):
        """Constructor de la clase my_papi que recibe por parametro la 
        localizacion de la liberia libmy_papi.so."""

        super(my_papi, self).__init__()

        # Loads the library path
        self.__set_my_lib(path)

        # Establish the warning format
        warnings.formatwarning = self.__warning_on_one_line
    # ----------------------------------------------------------------------- #

    def prepare_measure(self, events_file, cpus=None):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Params for the functions
        # ------------------------------------------------------------------- #
        input_file_name = events_file.encode('utf-8')
        num_cpus = c_int()
        # cpus
        num_event_sets = c_int()
        event_sets = c_int()

        # Setup the params
        if cpus is None:
            num_cpus = c_int(1)
        else:
            num_cpus = c_int(len(cpus))
            # Cast the cpu list to: int*
            aux = cpus
            cpus = (c_int * num_cpus.value)(*aux)
        num_event_sets = num_cpus

        # ------------------------------------------------------------------- #
        # Call for the functions
        # ------------------------------------------------------------------- #
        self.p_lib.my_prepare_measure(input_file_name, num_cpus, cpus, 
                                      num_event_sets, byref(event_sets))

        # We need to save the event_sets for start and stop the measure
        self.event_sets = event_sets
        self.cpus = cpus
    # ----------------------------------------------------------------------- #

    def start_measure(self):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Params for the functions
        # ------------------------------------------------------------------- #
        num_event_sets = c_int()
        event_sets = c_int()

        # Setup the params
        if self.cpus is None:
            num_event_sets = c_int(1)
        else:
            num_event_sets = c_int(len(self.cpus))
        event_sets = self.event_sets

        # ------------------------------------------------------------------- #
        # Call for the functions
        # ------------------------------------------------------------------- #
        self.p_lib.my_start_measure(num_event_sets, byref(event_sets))
    # ----------------------------------------------------------------------- #

    def stop_measure(self):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Params for the functions
        # ------------------------------------------------------------------- #
        num_event_sets = c_int()
        event_sets = c_int()
        values = POINTER(c_longlong)()

        # Setup the params
        if self.cpus is None:
            num_event_sets = c_int(1)
        else:
            num_event_sets = c_int(len(self.cpus))
        event_sets = self.event_sets

        # ------------------------------------------------------------------- #
        # Call for the functions
        # ------------------------------------------------------------------- #
        self.p_lib.my_stop_measure(num_event_sets, byref(event_sets), 
                                   byref(values))
        # We need to save the event_sets for start and stop the measure
        self.values = values
    # ----------------------------------------------------------------------- #

    def print_measure(self, file_name=None):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Params for the functions
        # ------------------------------------------------------------------- #
        num_cpus = c_int()
        cpus = c_int()
        values = POINTER(c_longlong)()

        # Setup the params
        if self.cpus is None:
            num_cpus = c_int(1)
            cpus = None
        else:
            num_cpus = c_int(len(self.cpus))
            cpus = self.cpus

        if file_name is not None:
            output_file_name = file_name.encode('utf-8')
        else:
            output_file_name = file_name

        values = self.values

        # ------------------------------------------------------------------- #
        # Call for the functions
        # ------------------------------------------------------------------- #
        self.p_lib.my_print_measure(num_cpus, cpus, byref(values), 
                                   output_file_name)
        
        # ------------------------------------------------------------------- #
        # Run the my_free_measure() function too
        # ------------------------------------------------------------------- #
        # num_event_sets = c_int(num_cpus.value)
        # self.p_lib.my_free_measure(byref(values), num_event_sets)
    # ----------------------------------------------------------------------- #

    def end_measure(self):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Call for the functions
        # ------------------------------------------------------------------- #
        self.p_lib.my_PAPI_shutdown()
    # ----------------------------------------------------------------------- #

    def __load_functions(self):
        """Creates the main functions that may be used for the user."""

        # ------------------------------------------------------------------- #
        # int my_prepare_measure(char *input_file_name, int num_cpus, 
        #                       int *cpus, int num_event_sets, int *event_sets)
        # ------------------------------------------------------------------- #
        self.p_lib.my_prepare_measure.argtypes = [c_char_p, c_int, 
                                        POINTER(c_int), c_int, POINTER(c_int)]
        self.p_lib.my_prepare_measure.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_start_measure(int num_event_sets, int *event_sets)
        # ------------------------------------------------------------------- #
        self.p_lib.my_start_measure.argtypes = [c_int, POINTER(c_int)]
        self.p_lib.my_start_measure.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_stop_measure(int num_event_sets, int *event_sets, 
        #                     long long **values)
        # ------------------------------------------------------------------- #
        self.p_lib.my_stop_measure.argtypes = [c_int, POINTER(c_int), 
                                               POINTER(POINTER(c_longlong))]
        self.p_lib.my_stop_measure.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_print_measure(int num_cpus, int *cpus, long long **values,
        #                      char *output_file_name)
        # ------------------------------------------------------------------- #
        self.p_lib.my_print_measure.argtypes = [c_int, POINTER(c_int), 
                                        POINTER(POINTER(c_longlong)), c_char_p]
        self.p_lib.my_print_measure.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_free_measure(long long **values, int num_event_sets)
        # ------------------------------------------------------------------- #
        # self.p_lib.my_free_measure.argtypes = [POINTER(POINTER(c_longlong)), 
        #                                        c_int]
        # self.p_lib.my_free_measure.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # void my_PAPI_shutdown(void)
        # ------------------------------------------------------------------- #
        self.p_lib.my_PAPI_shutdown.argtypes = None
        self.p_lib.my_PAPI_shutdown.restype = None
        # ------------------------------------------------------------------- #
    # ----------------------------------------------------------------------- #

    def __set_my_lib(self, libname):
        """Carga la libreria de libmy_papi.so, para ello es necesario 
        indicar su PATH."""

        # Load the shared library into ctypes
        print(libname)
        self.p_lib = CDLL(libname)
        self.__load_functions()
    # ----------------------------------------------------------------------- #

    def __warning_on_one_line(self, message, category, filename, lineno,
                              file=None, line=None):
        """Format the warning output."""

        return '%s:%s:\n\t%s: %s\n' % (filename, lineno, category.__name__,
                                       message)
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    # define Python user-defined exceptions

    class Error(Exception):
        """Base class for other exceptions"""
        pass

    class NoMeasureFinishedError(Error):
        """Raised when there is no result obtained."""
        pass

    class WrongParameterError(Error):
        """Raised when there is an incorrect parameter."""
        pass
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

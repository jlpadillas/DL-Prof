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
    # self.cores          # Array de cores logicos pertenecientes al mismo fisico
    # self.p_lib          # Con el se puede acceder a la liberia y sus func.
    # self.num_event_sets # numero de event_sets
    # self.event_sets     # lista con los event_sets
    # self.num_cpus       # num de cpus
    # self.cpus           # lista con las cpus
    # self.values           # lista con los resultados

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
        # We need to save the event_sets for start and stop the measure
        input_file_name = events_file.encode('utf-8')
        # self.num_cpus = c_int()
        # self.cpus
        self.num_event_sets = c_int()
        self.event_sets = c_int()
        print("event_sets = ", self.event_sets._b_needsfree_)

        # Setup the params
        if cpus is None:
            self.num_cpus = c_int(1)
            self.cpus = cpus
        else:
            self.num_cpus = c_int(len(cpus))
            # Cast the cpu list to: int*
            aux = cpus.copy()
            self.cpus = (c_int * self.num_cpus.value)(*aux)
        self.num_event_sets = self.num_cpus


        print("len(cpus) = ", self.num_cpus.value)
        print("list(self.cpus) = ", list(self.cpus))
        print("num_event_sets = ", self.num_event_sets.value)
        print("event_sets = ", byref(self.event_sets))

        # ------------------------------------------------------------------- #
        # Calling the function
        # ------------------------------------------------------------------- #
        self.p_lib.my_prepare_measure(input_file_name, self.num_cpus,
                                      self.cpus, self.num_event_sets,
                                      byref(self.event_sets))

        print("event_sets = ", self.event_sets.contents)
    # ----------------------------------------------------------------------- #

    def start_measure(self):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Calling the function
        # ------------------------------------------------------------------- #
        self.p_lib.my_start_measure(self.num_event_sets,
                                    byref(self.event_sets))
    # ----------------------------------------------------------------------- #

    def stop_measure(self):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Params for the functions
        # ------------------------------------------------------------------- #
        self.values = POINTER(c_longlong)()

        # ------------------------------------------------------------------- #
        # Calling the function
        # ------------------------------------------------------------------- #
        self.p_lib.my_stop_measure(self.num_event_sets, byref(self.event_sets),
                                   byref(self.values))
    # ----------------------------------------------------------------------- #

    def print_measure(self, file_name=None):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Params for the functions
        # ------------------------------------------------------------------- #
        if file_name is None:
            output_file_name = file_name
        else:
            output_file_name = file_name.encode('utf-8')

        # ------------------------------------------------------------------- #
        # Calling the function
        # ------------------------------------------------------------------- #
        self.p_lib.my_print_measure(self.num_cpus, self.cpus, byref(self.values),
                                    output_file_name)

    def end_measure(self):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Run the my_free_measure() function too
        # ------------------------------------------------------------------- #
        # self.p_lib.my_free_measure(byref(self.values), self.num_event_sets)

        # ------------------------------------------------------------------- #
        # Calling the function
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
                                                  POINTER(c_int), c_int,
                                                  POINTER(c_int)]
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
                                                POINTER(POINTER(c_longlong)),
                                                c_char_p]
        self.p_lib.my_print_measure.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_free_measure(long long **values, int num_event_sets)
        # ------------------------------------------------------------------- #
        self.p_lib.my_free_measure.argtypes = [POINTER(POINTER(c_longlong)),
                                               c_int]
        self.p_lib.my_free_measure.restype = c_int
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

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
    # self.event_sets     # lista con los event_setss

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

        self.events_file = events_file

        # ------------------------------------------------------------------- #
        # Params for the functions
        # ------------------------------------------------------------------- #
        # We need to save the event_sets for start and stop the measure
        input_file_name = events_file.encode('utf-8')

        if cpus is None:
            self.num_cpus = c_int(1)
            self.cpus = cpus
        else:
            self.num_cpus = c_int(len(cpus))
            # Cast the cpu list to: int*
            self.cpus = (c_int * self.num_cpus.value)(*cpus)

        # ------------------------------------------------------------------- #
        # Calling the function
        # ------------------------------------------------------------------- #
        self.p_lib.my_prepare_measure(input_file_name, self.num_cpus,
                                      self.cpus)
    # ----------------------------------------------------------------------- #

    def start_measure(self):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Calling the function
        # ------------------------------------------------------------------- #
        self.p_lib.my_start_measure()
    # ----------------------------------------------------------------------- #

    def stop_measure(self):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Calling the function
        # ------------------------------------------------------------------- #
        self.p_lib.my_stop_measure()
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
        self.p_lib.my_print_measure(output_file_name)

    def finalize_measure(self):
        """Gets the events to be measured and starts it."""

        # ------------------------------------------------------------------- #
        # Calling the function
        # ------------------------------------------------------------------- #
        self.p_lib.my_finalize_measure()
    # ----------------------------------------------------------------------- #

    def check_results(self, file_name):
        """"""

        import pandas as pd

        # Read events from file
        with open(self.events_file) as f:
            events = f.read().splitlines()

        # Read csv
        data = pd.read_csv(file_name, header=None, sep=":", names=range(4))

        # Assign new header
        header = ["CPU", "Value", "Unit", "Event Name"]
        data.columns = header

        # Sum of the same events
        events_sum = {}
        for e in events:
            sum = data.loc[data["Event Name"] == e, "Value"].sum()
            events_sum[e] = sum

        # Print the sum of the events
        locale.setlocale(locale.LC_ALL, '')

        for k,v in events_sum.items():
            print("Sum [",k,"] =",locale.format_string('%.0f', v, True))
    # ----------------------------------------------------------------------- #

    def __load_functions(self):
        """Creates the main functions that may be used for the user."""

        # ------------------------------------------------------------------- #
        # int my_prepare_measure(char *input_file_name, int num_cpus,
        #                       int *cpus)
        # ------------------------------------------------------------------- #
        self.p_lib.my_prepare_measure.argtypes = [c_char_p, c_int,
                                                  POINTER(c_int)]
        self.p_lib.my_prepare_measure.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_start_measure()
        # ------------------------------------------------------------------- #
        self.p_lib.my_start_measure.argtypes = None
        self.p_lib.my_start_measure.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_stop_measure()
        # ------------------------------------------------------------------- #
        self.p_lib.my_stop_measure.argtypes = None
        self.p_lib.my_stop_measure.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_print_measure(char *output_file_name)
        # ------------------------------------------------------------------- #
        self.p_lib.my_print_measure.argtypes = [c_char_p]
        self.p_lib.my_print_measure.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_finalize_measure()
        # ------------------------------------------------------------------- #
        self.p_lib.my_finalize_measure.argtypes = None
        self.p_lib.my_finalize_measure.restype = c_int
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

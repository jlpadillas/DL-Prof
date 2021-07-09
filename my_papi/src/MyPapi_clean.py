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

# Imports for the module
from ctypes import CDLL, c_int, c_char_p, POINTER

# --------------------------------------------------------------------------- #

class MyPapi(object):
    """
    Class that uses the libmy_papi.so library and perform measures of events.
    It is based on the Performance Application Programming Interface (PAPI).

    Attributes
    ----------
    self.p_lib : ctypes.CDLL
        Library of my_papi
    self.cpus : list
        List of int where the system will measure the events
    self.events_file : str
        Path where the file with the events is located
    self.output_file : str
        Path where the file with the results is located
    """

    def __init__(self, lib_path):
        """
        My_papi class constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        """

        super(MyPapi, self).__init__()

        # Loads the library path
        self.__set_my_lib(lib_path)
    # ----------------------------------------------------------------------- #

    def prepare_measure(self, events_file, cpus=None):
        """It performs the necessary adjustments before start measuring.

        A file path is passed as a parameter where the events to be measured
        are distributed one per line.

        If the argument `cpus` isn't passed in, then the default CPUs to be
        measured will be all the logical cores of the system.

        Parameters
        ----------
        events_file : str
            Path where the file is located
        cpus : list, optional
            List of integers which corresponds to the cpus where we have to
            measure the events (default is all)
        """

        if cpus is None:
            import multiprocessing
            cpus = list(range(0, multiprocessing.cpu_count()))

        # Saving the passed arguments
        self.events_file = events_file
        self.cpus = cpus

        # Now, we have to cast the data to pass them to the C library
        # 1. Encode the string
        # 2. Create a c_int type with the length of the cpu list
        # 3. Cast the cpu list to: int*
        len_cpus = len(cpus)
        self.p_lib.my_prepare_measure(events_file.encode('utf-8'),
                                      c_int(len_cpus),
                                      (c_int * len_cpus)(*cpus))
    # ----------------------------------------------------------------------- #

    def start_measure(self):
        """Calls the C function with the same name and start the measuring.

        Parameters
        ----------
        None
        """

        self.p_lib.my_start_measure()
    # ----------------------------------------------------------------------- #

    def stop_measure(self):
        """Calls the C function with the same name and stop the measuring.

        Parameters
        ----------
        None
        """

        self.p_lib.my_stop_measure()
    # ----------------------------------------------------------------------- #

    def print_measure(self, output_file=None):
        """Print the results to the screen or to a file.

        If the argument `output_file` isn't passed in, then the default output
        is the screen.

        Parameters
        ----------
        output_file : str, optional
            Path (and name) of the file where the results will be printed.
        """

        self.output_file = output_file
        if output_file is not None:
            output_file = output_file.encode('utf-8')

        self.p_lib.my_print_measure(output_file)
    # ----------------------------------------------------------------------- #

    def finalize_measure(self):
        """Calls the C function with the same name which will stop the my_papi
        library and free the memory used.

        Parameters
        ----------
        None
        """

        self.p_lib.my_finalize_measure()
    # ----------------------------------------------------------------------- #

    def __set_my_lib(self, lib_path):
        """
        Loads the library libmy_papi.so from the PATH passed by parameter and
        define the input/output of the main functions.

        Parameters
        ----------
        lib_path : Path
            Path to the library
        """

        self.p_lib = CDLL(lib_path)

        # ------------------------------------------------------------------- #
        # int my_prepare_measure(char *input_file_name, int num_cpus,
        #                       int *cpus)
        # ------------------------------------------------------------------- #
        self.p_lib.my_prepare_measure.argtypes = [
            c_char_p, c_int, POINTER(c_int)]
        self.p_lib.my_prepare_measure.restype = c_int

        # ------------------------------------------------------------------- #
        # int my_start_measure()
        # ------------------------------------------------------------------- #
        self.p_lib.my_start_measure.argtypes = None
        self.p_lib.my_start_measure.restype = c_int

        # ------------------------------------------------------------------- #
        # int my_stop_measure()
        # ------------------------------------------------------------------- #
        self.p_lib.my_stop_measure.argtypes = None
        self.p_lib.my_stop_measure.restype = c_int

        # ------------------------------------------------------------------- #
        # int my_print_measure(char *output_file_name)
        # ------------------------------------------------------------------- #
        self.p_lib.my_print_measure.argtypes = [c_char_p]
        self.p_lib.my_print_measure.restype = c_int

        # ------------------------------------------------------------------- #
        # int my_finalize_measure()
        # ------------------------------------------------------------------- #
        self.p_lib.my_finalize_measure.argtypes = None
        self.p_lib.my_finalize_measure.restype = c_int
    # ----------------------------------------------------------------------- #

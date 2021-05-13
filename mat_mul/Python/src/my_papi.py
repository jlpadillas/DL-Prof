#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
import locale
import warnings
from datetime import datetime

# 3rd party packages
from ctypes import *
from tensorflow import keras

# local source

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
# Variables used between the classes

# Path to the 'libmy_papi.so' library
_library_file = None

# Path to the file where the events are
_events_file = None

# --------------------------------------------------------------------------- #


class my_papi(object):
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

    """

    def __init__(self, lib_path):
        """
        My_papi Class Constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        """

        super(my_papi, self).__init__()

        # Loads the library path
        self.__set_my_lib(lib_path)

        # Establish the warning format
        warnings.formatwarning = self.__warning_on_one_line
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

    def check_results(self, file_name):
        """Test the values in the file and check the total amount of each event
        """

        import pandas as pd

        # Setting the dict of event name and how many computations represent
        # each count
        computations_dict = {
            "fp_arith_inst_retired.128b_packed_double": 2,
            "fp_arith_inst_retired.128b_packed_single": 4,
            "fp_arith_inst_retired.256b_packed_double": 4,
            "fp_arith_inst_retired.256b_packed_single": 8,
            "fp_arith_inst_retired.512b_packed_double": 8,
            "fp_arith_inst_retired.512b_packed_single": 16,
            "fp_arith_inst_retired.scalar_double": 1,
            "fp_arith_inst_retired.scalar_single": 1,
            "fp_assist.any": 1
        }

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
        total_fp_events = 0
        for k, v in events_sum.items():
            print("Sum [", k, "] =", locale.format_string('%.0f', v, True))
            if computations_dict.get(k) is not None:
                total_fp_events += computations_dict[k] * v
        print("Total fp measured =", locale.format_string('%.0f',
                                                          total_fp_events, True))
    # ----------------------------------------------------------------------- #

    def create_table(self, file_name):
        """Test the values in the file and check the total amount of each event
        """

        import plotly.graph_objects as go
        import pandas as pd

        # Read events from file
        with open(self.events_file) as f:
            events = f.read().splitlines()

        # Read csv
        df = pd.read_csv(file_name, header=None, sep=":", names=range(4))

        # Assign new header
        header = ["CPU", "Value", "Unit", "Event Name"]
        df.columns = header

        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=df["CPU"],
                       fill_color='lavender',
                       align='left'))
        ])

        fig.write_html("out/file.html")
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

        _lib_path = lib_path
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

        # ------------------------------------------------------------------- #
        # void my_PAPI_shutdown(void)
        # ------------------------------------------------------------------- #
        self.p_lib.my_PAPI_shutdown.argtypes = None
        self.p_lib.my_PAPI_shutdown.restype = None
    # ----------------------------------------------------------------------- #

    def __warning_on_one_line(self, message, category, filename, lineno,
                              file=None, line=None):
        """Format the warning output."""

        return '%s:%s:\n\t%s: %s\n' % (filename, lineno, category.__name__,
                                       message)
    # ----------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #


class my_callbacks_on_epochs(keras.callbacks.Callback):
    """
    Custom callback to run with my_papi library and measures the system in each
    epoch.

    Attributes
    ----------
    self.cores : int
        Number of logical cores of the system
    self.p_lib : CDLL
        Library of my_papi

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes

    """

    def __init__(self, path_to_lib, events_file):
        """
        Class Constructor to initialize the object.

        Parameters
        ----------
        lib_path : Path
            Path to the library
        """

        super(my_callbacks_on_epochs, self).__init__()

        # Creates an object of the class my_papi
        self.mp = my_papi(path_to_lib)

        # Prepares the measure on all cpus
        cpus = list(range(0, int(self.mp.get_num_logical_cores())))
        self.mp.prepare_measure(events_file, cpus)
        # ! Path were the results will be stored
        self.path = "out/"
        self.extension = ".csv"

    # ------------------------- Epoch-level methods ------------------------- #
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the beginning of an epoch during training."""

        # Creates a csv name depending on the starting date
        self.start_time = datetime.now()
        self.output_file = self.path + __name__ + "_" + \
            self.start_time.strftime("%Y-%m-%d_%H:%M:%S") + "_epoch-" + \
            str(epoch) + self.extension

        # Starts the measure with my_papi library
        self.mp.start_measure()
    # ----------------------------------------------------------------------- #

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        # Stops the measure with my_papi library
        self.mp.stop_measure()

        # Saves time of finish
        # self.stop_time = datetime.now()

        # Saves the results on a file
        self.mp.print_measure(self.output_file)

        # Finalize the measure
        self.mp.finalize_measure()
    # ----------------------------------------------------------------------- #
    # ----------------------- END Epoch-level methods ----------------------- #
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
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
# --------------------------------------------------------------------------- #

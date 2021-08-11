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
from locale import setlocale, format_string, LC_ALL


# Sets the locale for future prints
import os
import pandas as pd

# Forces the program to execute on CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# Just disables the warning, doesn't take advantage of AVX/FMA to run faster
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Last import or warnning will appear on screen (libcudart not found)
from tensorflow import keras
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

        # _library_file = lib_path
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

# --------------------------------------------------------------------------- #

class MyCallbacks(keras.callbacks.Callback):
    """
    Abstact class which have custom callbacks to use with my_papi library.

    Attributes
    ----------
    self.mp : my_papi
        Oject of the class my_papi
    self.output_file : str
        Path (and name) of the file where the results will be printed. If it's
        `None`, then the results will be printed on screen
    """

    def __init__(self, lib_path, events_file, output_file=None):
        """
        My_callbacks class constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        events_file : str
            Path where the file, with the events to be measured, is located
        output_file : str, optional
            Path (and name) of the file where the results will be printed. If
            `None` is passed, then the results will be printed on screen
        """

        super(MyCallbacks, self).__init__()

        # Creates an object of the class my_papi
        self.mp = MyPapi(lib_path=lib_path)

        # Prepares the measure on ALL cpus
        # ! modify this to get the num of cpus automatic
        # cpus = None
        self.cpus = list(range(2, 32))
        # self.cpus = [2]
        self.mp.prepare_measure(events_file=events_file, cpus=self.cpus)

        # Save the output file variable for later
        self.output_file = output_file

        # We have to decompose the path, name and extension of the output file
        if self.output_file is not None:
            # Gets an array with head + tail: path + file_name
            self.head_tail = os.path.split(output_file)
            self.name_extension = os.path.splitext(self.head_tail[1])

    # --------------------------- Global methods ---------------------------- #
    def on_train_begin(self, logs=None):
        """Called at the beginning of fit."""

        pass

    def on_train_end(self, logs=None):
        """Called at the end of fit."""

        pass

    def on_test_begin(self, logs=None):
        """Called at the beginning of evaluate."""

        pass

    def on_test_end(self, logs=None):
        """Called at the end of evaluate."""

        pass

    def on_predict_begin(self, logs=None):
        """Called at the beginning of predict."""

        pass

    def on_predict_end(self, logs=None):
        """Called at the end of predict."""

        pass
    # ------------------------- END Global methods -------------------------- #

    # ------------------------- Batch-level methods ------------------------- #
    def on_train_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during training."""

        pass

    def on_train_batch_end(self, batch, logs=None):
        """Called at the end of training a batch. Within this method, logs is a
        dict containing the metrics results."""

        pass

    def on_test_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during testing."""

        pass

    def on_test_batch_end(self, batch, logs=None):
        """Called at the end of testing a batch. Within this method, logs is a
        dict containing the metrics results."""

        pass

    def on_predict_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during predicting."""

        pass

    def on_predict_batch_end(self, batch, logs=None):
        """Called at the end of predicting a batch. Within this method, logs is
        a dict containing the metrics results."""

        pass
    # ----------------------- END Batch-level methods ----------------------- #

    # ------------------------- Epoch-level methods ------------------------- #
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the beginning of an epoch during training."""

        pass

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        pass
    # ----------------------- END Epoch-level methods ----------------------- #

    def finalize_measure(self):
        """Ends the measure."""

        self.mp.finalize_measure()
# --------------------------------------------------------------------------- #

class MeasureOnTrainPhase(MyCallbacks):
    """
    Custom callback to run with my_papi library and measures the system in the
    training phase.

    Attributes
    ----------
    self.mp : my_papi
        Oject of the class my_papi
    self.output_file : str
        Path (and name) of the file where the results will be printed. If it's
        `None`, then the results will be printed on screen
    """

    def __init__(self, lib_path, events_file, output_file=None):
        """
        Class Constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        events_file : str
            Path where the file, with the events to be measured, is located
        output_file : str, optional
            Path (and name) of the file where the results will be printed. If
            `None` is passed, then the results will be printed on screen
        """

        super(MeasureOnTrainPhase, self).__init__(events_file=events_file,
                                                  lib_path=lib_path,
                                                  output_file=output_file)

    # --------------------------- Global methods ---------------------------- #
    def on_train_begin(self, logs=None):
        """Called at the beginning of fit."""

        # Starts the measure with my_papi library
        self.mp.start_measure()

    def on_train_end(self, logs=None):
        """Called at the end of fit."""

        # Stops the measure with my_papi library
        self.mp.stop_measure()

        # Saves the results on a file
        self.mp.print_measure(self.output_file)
    # ------------------------- END Global methods -------------------------- #
# --------------------------------------------------------------------------- #

class MeasureOnEachEpoch(MyCallbacks):
    """
    Custom callback to run with my_papi library and measures the system in each
    epoch.

    Attributes
    ----------
    self.mp : my_papi
        Oject of the class my_papi
    self.output_file : str
        Path (and name) of the file where the results will be printed. If it's
        `None`, then the results will be printed on screen
    """

    def __init__(self, lib_path, events_file, output_file=None):
        """
        Class Constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        events_file : str
            Path where the file, with the events to be measured, is located
        output_file : str, optional
            Path (and name) of the file where the results will be printed. If
            `None` is passed, then the results will be printed on screen
        """

        super(MeasureOnEachEpoch, self).__init__(events_file=events_file,
                                                 lib_path=lib_path,
                                                 output_file=output_file)

    # ------------------------- Epoch-level methods ------------------------- #
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the beginning of an epoch during training."""

        # Starts the measure with my_papi library
        self.mp.start_measure()

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        # Stops the measure with my_papi library
        self.mp.stop_measure()

        # Saves the results on a file
        self.mp.print_measure(self.output_file)
    # ----------------------- END Epoch-level methods ----------------------- #
# --------------------------------------------------------------------------- #

class MeasureOnDeterminedEpoch(MyCallbacks):
    """
    Custom callback to run with my_papi library and measures the system in each
    epoch.

    Attributes
    ----------
    self.mp : my_papi
        Oject of the class my_papi
    self.output_file : str
        Path (and name) of the file where the results will be printed. If it's
        `None`, then the results will be printed on screen
    """

    def __init__(self, lib_path, events_file, output_file=None):
        """
        Class Constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        events_file : str
            Path where the file, with the events to be measured, is located
        output_file : str, optional
            Path (and name) of the file where the results will be printed. If
            `None` is passed, then the results will be printed on screen
        """

        super(MeasureOnDeterminedEpoch, self).__init__(events_file=events_file,
                                                 lib_path=lib_path,
                                                 output_file=output_file)

    # ------------------------- Epoch-level methods ------------------------- #
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the beginning of an epoch during training."""

        if epoch == 2:
          # Starts the measure with my_papi library
          self.mp.start_measure()

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        if epoch == 2:
          # Stops the measure with my_papi library
          self.mp.stop_measure()

          # Saves the results on a file
          self.mp.print_measure(self.output_file)
    # ----------------------- END Epoch-level methods ----------------------- #
# --------------------------------------------------------------------------- #

class MeasureOnEachBatch(MyCallbacks):
    """
    Custom callback to run with my_papi library and measures the system in each
    batch.

    Attributes
    ----------
    self.mp : my_papi
        Oject of the class my_papi
    self.output_file : str
        Path (and name) of the file where the results will be printed. If it's
        `None`, then the results will be printed on screen
    """

    def __init__(self, lib_path, events_file, output_file=None):
        """
        Class Constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        events_file : str
            Path where the file, with the events to be measured, is located
        output_file : str, optional
            Path (and name) of the file where the results will be printed. If
            `None` is passed, then the results will be printed on screen
        """

        super(MeasureOnEachBatch, self).__init__(events_file=events_file,
                                                 lib_path=lib_path,
                                                 output_file=output_file)

    # ------------------------- Batch-level methods ------------------------- #
    def on_train_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during training."""

        # Starts the measure with my_papi library
        self.mp.start_measure()

    def on_train_batch_end(self, batch, logs=None):
        """Called at the end of training a batch. Within this method, logs is a
        dict containing the metrics results."""

        # Stops the measure with my_papi library
        self.mp.stop_measure()

        # Saves the results on a file
        self.mp.print_measure(self.output_file)

    def on_test_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during testing."""
        pass

    def on_test_batch_end(self, batch, logs=None):
        """Called at the end of testing a batch. Within this method, logs is a
        dict containing the metrics results."""
        pass

    def on_predict_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during predicting."""
        pass

    def on_predict_batch_end(self, batch, logs=None):
        """Called at the end of predicting a batch. Within this method, logs is
        a dict containing the metrics results."""
        pass
    # ----------------------- END Batch-level methods ----------------------- #
# --------------------------------------------------------------------------- #

class MeasureEpochAndBatch(keras.callbacks.Callback):
    """
    Custom callback to run with my_papi library and measures the system in each
    epoch.

    Attributes
    ----------
    self.mp : my_papi
        Oject of the class my_papi
    self.output_file : str
        Path (and name) of the file where the results will be printed. If it's
        `None`, then the results will be printed on screen
    """

    def __init__(self, lib_path, events_file, output_file=None):
        """
        Class Constructor to initialize the object.

        Parameters
        ----------
        lib_path : str
            Path to the shared library libmy_papi.so
        events_file : str
            Path where the file, with the events to be measured, is located
        output_file : str, optional
            Path (and name) of the file where the results will be printed. If
            `None` is passed, then the results will be printed on screen
        """

        super(MeasureEpochAndBatch, self).__init__()

        # Creates two objects of the class my_papi
        self.mp_epoch = MyPapi(lib_path=lib_path)
        self.mp_batch = MyPapi(lib_path=lib_path)

        # Prepares the measure on ALL cpus
        # ! modify this to get the num of cpus automatic
        # cpus = None
        self.cpus = list(range(2, 32))
        self.mp_epoch.prepare_measure(events_file=events_file, cpus=self.cpus)
        self.mp_batch.prepare_measure(events_file=events_file, cpus=self.cpus)

        # Save the output file variable for later
        self.output_file = output_file

        # We have to decompose the path, name and extension of the output file
        if self.output_file is not None:
            # Gets an array with head + tail: path + file_name
            self.head_tail = os.path.split(output_file)
            self.name_extension = os.path.splitext(self.head_tail[1])

            # From the file indicated, generate a new file
            self.batch_output_file = self.head_tail[0] + "/" + str(self.name_extension[0]
            + "_batch" + self.name_extension[1])
        else:
            self.batch_output_file = None
        # Just measure the batches indicated
        self.measure_batch = True

    # ------------------------- Batch-level methods ------------------------- #
    def on_train_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during training."""

        if self.measure_batch:
            self.mp_batch.start_measure()

    def on_train_batch_end(self, batch, logs=None):
        """Called at the end of training a batch. Within this method, logs is a
        dict containing the metrics results."""

        if self.measure_batch:
            self.mp_batch.stop_measure()
            self.mp_batch.print_measure(self.batch_output_file)
    # ----------------------- END Batch-level methods ----------------------- #

    # ------------------------- Epoch-level methods ------------------------- #
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the beginning of an epoch during training."""

        print("Begin del epoch", epoch)

        if epoch == 1:
            self.measure_batch = False

        # Starts the measure with my_papi library
        self.mp_epoch.start_measure()

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        print("\nEnd del epoch", epoch)

        # Stops the measure with my_papi library
        self.mp_epoch.stop_measure()

        # Saves the results on a file
        self.mp_epoch.print_measure(self.output_file)

        # if epoch == 1:
        #     self.measure_batch = False
    # ----------------------- END Epoch-level methods ----------------------- #
# --------------------------------------------------------------------------- #

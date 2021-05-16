#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
from tensorflow import keras

# 3rd party packages

# local source
from MyPapi import MyPapi

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


class Callbacks(keras.callbacks.Callback):
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

        super(Callbacks, self).__init__()

        # Creates an object of the class my_papi
        self.mp = MyPapi(lib_path=lib_path)

        # Prepares the measure on ALL cpus
        self.mp.prepare_measure(events_file=events_file, cpus=None)

        # Save the output file variable for later
        self.output_file = output_file

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


class MeasureOnEachEpoch(Callbacks):
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


class MeasureOnEachBatch(Callbacks):
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

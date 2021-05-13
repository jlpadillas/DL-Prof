#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
from abc import abstractmethod, ABC
from datetime import datetime
from tensorflow import keras

# 3rd party packages

# local source
from my_papi import my_papi

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


class my_callbacks(keras.callbacks.Callback, ABC):
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

        super(my_callbacks, self).__init__()

        # Creates an object of the class my_papi
        self.mp = my_papi(lib_path=lib_path)

        # Prepares the measure on ALL cpus
        self.mp.prepare_measure(events_file=events_file, cpus=None)

        # Save the variable for later
        self.output_file = output_file

    # --------------------------- Global methods ---------------------------- #
    @abstractmethod
    def on_train_begin(self, logs=None):
        """Called at the beginning of fit."""

        pass

    @abstractmethod
    def on_train_end(self, logs=None):
        """Called at the end of fit."""

        pass

    @abstractmethod
    def on_test_begin(self, logs=None):
        """Called at the beginning of evaluate."""

        pass

    @abstractmethod
    def on_test_end(self, logs=None):
        """Called at the end of evaluate."""

        pass

    @abstractmethod
    def on_predict_begin(self, logs=None):
        """Called at the beginning of predict."""

        pass

    @abstractmethod
    def on_predict_end(self, logs=None):
        """Called at the end of predict."""

        pass
    # ------------------------- END Global methods -------------------------- #

    # ------------------------- Batch-level methods ------------------------- #
    @abstractmethod
    def on_train_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during training."""

        pass

    @abstractmethod
    def on_train_batch_end(self, batch, logs=None):
        """Called at the end of training a batch. Within this method, logs is a
        dict containing the metrics results."""

        pass

    @abstractmethod
    def on_test_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during testing."""

        pass

    @abstractmethod
    def on_test_batch_end(self, batch, logs=None):
        """Called at the end of testing a batch. Within this method, logs is a
        dict containing the metrics results."""

        pass

    @abstractmethod
    def on_predict_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during predicting."""

        pass

    @abstractmethod
    def on_predict_batch_end(self, batch, logs=None):
        """Called at the end of predicting a batch. Within this method, logs is
        a dict containing the metrics results."""

        pass
    # ----------------------- END Batch-level methods ----------------------- #

    # ------------------------- Epoch-level methods ------------------------- #
    @abstractmethod
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the beginning of an epoch during training."""

        pass

    @abstractmethod
    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        pass
    # ----------------------- END Epoch-level methods ----------------------- #

    def finalize_measure(self):
        """Ends the measure."""

        self.mp.finalize_measure()
# --------------------------------------------------------------------------- #


class my_callbacks_on_epochs(my_callbacks):
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

        super(my_callbacks_on_epochs, self).__init__(events_file=events_file,
                                                     lib_path=lib_path)

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

        # Creates a csv name depending on the starting date
        self.start_time = datetime.now()
        self.output_file = self.out_dir + __name__ + "_" + \
            self.start_time.strftime("%Y-%m-%d_%H:%M:%S") + "_epoch-" + \
            str(epoch) + self.extension

        # Starts the measure with my_papi library
        self.mp.start_measure()

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        # Stops the measure with my_papi library
        self.mp.stop_measure()

        # Saves end time ?
        # self.stop_time = datetime.now()

        # Saves the results on a file
        self.mp.print_measure(self.output_file)

    # ----------------------- END Epoch-level methods ----------------------- #
# --------------------------------------------------------------------------- #


# if __name__ == "__main__":

#     import pathlib

#     PWD = pathlib.Path(__file__).parent.parent.absolute()
#     CFG_DIR = PWD / "conf"
#     LIB_DIR = PWD / "lib"
#     OUT_DIR = PWD / "out"

#     lib_name = str(LIB_DIR / "libmy_papi.so")
#     event_file = str(CFG_DIR / "events_pc.cfg")

#     mc = my_callbacks_on_epochs(lib_name, event_file)

#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
from datetime import datetime

# 3rd party packages
from tensorflow import keras

# local source
from my_papi import my_papi

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


class my_callbacks_on_epochs(keras.callbacks.Callback):
    """Custom callback to use with my_papi library. This one measures each
    epoch."""

    # Attributes
    # ----------
    # self.mp          # Object of the clasee my_papi

    def __init__(self, path_to_lib, events_file):
        """Constructor"""

        super(my_callbacks_on_epochs, self).__init__()

        # Creates an object of the class my_papi
        self.mp = my_papi(path_to_lib)

        # Prepares the measure on all cpus
        cpus = list(range(0, int(self.mp.get_num_logical_cores())))
        self.mp.prepare_measure(events_file, cpus)
        # ! Path were the results will be stored
        self.path = "out/"
        self.extension = ".csv"
    # --------------------------- Global methods ---------------------------- #
    #
    # ------------------------- END Global methods -------------------------- #

    # ------------------------- Batch-level methods ------------------------- #
    #
    # ----------------------- END Batch-level methods ----------------------- #

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

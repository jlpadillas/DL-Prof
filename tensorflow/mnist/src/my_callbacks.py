#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library

# 3rd party packages
import tensorflow as tf
from tensorflow import keras

# local source

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


class my_callbacks(keras.callbacks.Callback):
    """Custom callbacks to use with my_papi library"""

    # --------------------------- Global methods ---------------------------- #
    def on_train_begin(self, logs=None):
        """Called at the beginning of fit."""

        keys = list(logs.keys())
        print("Starting training; got log keys: {}".format(keys))

    def on_train_end(self, logs=None):
        """Called at the end of fit."""

        keys = list(logs.keys())
        print("Stop training; got log keys: {}".format(keys))

    def on_test_begin(self, logs=None):
        """Called at the beginning of evaluate."""

        keys = list(logs.keys())
        print("Start testing; got log keys: {}".format(keys))

    def on_test_end(self, logs=None):
        """Called at the end of evaluate."""

        keys = list(logs.keys())
        print("Stop testing; got log keys: {}".format(keys))

    def on_predict_begin(self, logs=None):
        """Called at the beginning of predict."""

        keys = list(logs.keys())
        print("Start predicting; got log keys: {}".format(keys))

    def on_predict_end(self, logs=None):
        """Called at the end of predict."""

        keys = list(logs.keys())
        print("Stop predicting; got log keys: {}".format(keys))
    # ------------------------- END Global methods -------------------------- #

    # ------------------------- Batch-level methods ------------------------- #

    def on_train_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during training."""

        keys = list(logs.keys())
        print("...Training: start of batch {}; got log keys: {}".format(batch, keys))

    def on_train_batch_end(self, batch, logs=None):
        """Called at the end of training a batch. Within this method, logs is a
        dict containing the metrics results."""

        keys = list(logs.keys())
        print("...Training: end of batch {}; got log keys: {}".format(batch, keys))

    def on_test_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during testing."""

        keys = list(logs.keys())
        print("...Evaluating: start of batch {}; got log keys: {}".format(batch, keys))

    def on_test_batch_end(self, batch, logs=None):
        """Called at the end of testing a batch. Within this method, logs is a
        dict containing the metrics results."""

        keys = list(logs.keys())
        print("...Evaluating: end of batch {}; got log keys: {}".format(batch, keys))

    def on_predict_batch_begin(self, batch, logs=None):
        """Called right before processing a batch during predicting."""

        keys = list(logs.keys())
        print("...Predicting: start of batch {}; got log keys: {}".format(batch, keys))

    def on_predict_batch_end(self, batch, logs=None):
        """Called at the end of predicting a batch. Within this method, logs is
        a dict containing the metrics results."""

        keys = list(logs.keys())
        print("...Predicting: end of batch {}; got log keys: {}".format(batch, keys))

    # ----------------------- END Batch-level methods ----------------------- #

    # ------------------------- Epoch-level methods ------------------------- #
    def on_epoch_begin(self, epoch, logs=None):
        """Called at the beginning of an epoch during training."""

        keys = list(logs.keys())
        print("Start epoch {} of training; got log keys: {}".format(epoch, keys))

    def on_epoch_end(self, epoch, logs=None):
        """Called at the end of an epoch during training."""

        keys = list(logs.keys())
        print("End epoch {} of training; got log keys: {}".format(epoch, keys))
    # ----------------------- END Epoch-level methods ----------------------- #

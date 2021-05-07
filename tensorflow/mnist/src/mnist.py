#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
from tensorflow import keras
import os
import pathlib
import sys
import warnings

# 3rd party packages
import tensorflow as tf
assert tf.__version__ >= "2.0"


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


class mnist(object):
    """TODO."""

    # Attributes
    # ----------
    # self.cores          # Array de cores logicos pertenecientes al mismo fisico
    # self.p_lib          # Con el se puede acceder a la liberia y sus func.
    # self.num_event_sets # numero de event_sets
    # self.event_sets     # lista con los event_setss

    def __init__(self):
        """TODO."""

        super(self).__init__()

        # Forces the program to execute on CPU
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'

        # Just disables the warning, doesn't take advantage of AVX/FMA to run faster
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        # Establish the warning format
        warnings.formatwarning = self.__warning_on_one_line
    # ----------------------------------------------------------------------- #

    def set_parallelism():

        pass

    def fit(self):
        history = model.fit(X_train, y_train, epochs=1,
                            validation_data=(X_valid, y_valid))

        pass

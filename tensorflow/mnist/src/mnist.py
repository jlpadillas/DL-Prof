#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library

# 3rd party packages
from tensorflow import keras
import tensorflow as tf

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

        super(mnist, self).__init__()

        # Establish the warning format
        # warnings.formatwarning = self.__warning_on_one_line

        assert tf.__version__ >= "2.0"
    # ----------------------------------------------------------------------- #

    def setup(self):
        fashion_mnist = keras.datasets.fashion_mnist
        (X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

        self.X_valid, self.X_train = X_train_full[:5000] / \
            255., X_train_full[5000:] / 255.
        self.y_valid, self.y_train = y_train_full[:5000], y_train_full[5000:]
        X_test = X_test / 255.

        # class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
        #                "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

        self.model = keras.models.Sequential([
            keras.layers.Flatten(input_shape=[28, 28]),
            keras.layers.Dense(300, activation="relu"),
            keras.layers.Dense(100, activation="relu"),
            keras.layers.Dense(10, activation="softmax")
        ])

        self.model.compile(loss="sparse_categorical_crossentropy",
                           optimizer="sgd",
                           metrics=["accuracy"])

    def set_parallelism(self, inter=None, intra=None):
        """Parallalism is set to inter and intra"""

        inter_old = tf.config.threading.get_inter_op_parallelism_threads()
        intra_old = tf.config.threading.get_intra_op_parallelism_threads()

        if inter is not None and inter != inter_old:
            tf.config.threading.set_inter_op_parallelism_threads(inter)

        if intra is not None and intra != intra_old:
            tf.config.threading.set_intra_op_parallelism_threads(intra)

        print("inter_op_parallelis_threads =",
              tf.config.threading.get_inter_op_parallelism_threads(),
              "intra_op_parallelis_threads =",
              tf.config.threading.get_intra_op_parallelism_threads())

    def fit(self):
        self.history = self.model.fit(self.X_train, self.y_train, epochs=1,
                                      validation_data=(self.X_valid, self.y_valid))
        return self.history

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
        """setup"""

        # Fetch and load common datasets, including Fashion MNIST
        # It has the exact same format as MNIST (70.000 grayscale image of 28 x
        # 28 pixels each, with 10 classes).
        fashion_mnist = keras.datasets.fashion_mnist

        # Images represented as a 28 x 28 array
        # Pixel intensities are represented as integers (from 0 to 255)

        # The dataset is already split inot a training set and a test set
        (X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

        # We'll create a validation set
        # The validation set contains 5,000 images, and the test set contains 10,000 images:
        self.X_valid, self.X_train = X_train_full[:5000] / \
            255., X_train_full[5000:] / 255.
        self.y_valid, self.y_train = y_train_full[:5000], y_train_full[5000:]
        X_test = X_test / 255.

        # class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
        #                "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

        # Creating the model using the Sequential API
        # 1. Creates a Sequential model. Layers connected sequentially
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Flatten(input_shape=[28, 28]))
        self.model.add(keras.layers.Dense(300, activation="relu"))
        self.model.add(keras.layers.Dense(100, activation="relu"))
        self.model.add(keras.layers.Dense(10, activation="softmax"))
        

        self.model.compile(loss="sparse_categorical_crossentropy",
                           optimizer="sgd",
                           metrics=["accuracy"])
    # ----------------------------------------------------------------------- #

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
    # ----------------------------------------------------------------------- #

    def fit(self, my_batch_size=32, my_epoch=1, my_callbacks=None):
        # def fit(self):
        """Fit function"""

        self.history = self.model.fit(self.X_train, self.y_train,
                                      batch_size=my_batch_size,
                                      epochs=my_epoch,
                                      callbacks=my_callbacks,
                                      validation_data=(self.X_valid,
                                                       self.y_valid))
        return self.history
    # ----------------------------------------------------------------------- #

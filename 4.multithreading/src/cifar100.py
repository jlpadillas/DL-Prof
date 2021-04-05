#!/usr/bin/env python3
# coding: utf-8

# TensorFlow ≥2.0 is required
import os
from numpy.core.fromnumeric import size
import tensorflow as tf
from tensorflow.keras.datasets import cifar100
assert tf.__version__ >= "2.0"

from tensorflow import keras

# Parallalism is set to 1
# print(tf.config.threading.get_inter_op_parallelism_threads(), 
#     tf.config.threading.get_intra_op_parallelism_threads())

# tf.config.threading.set_inter_op_parallelism_threads(1)
# tf.config.threading.set_intra_op_parallelism_threads(1)

# print(tf.config.threading.get_inter_op_parallelism_threads(), 
#     tf.config.threading.get_intra_op_parallelism_threads())

# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# Just disables the warning, doesn't take advantage of AVX/FMA to run faster
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

cifar100 = keras.datasets.cifar100

(X_train_full, y_train_full), (X_test, y_test) = cifar100.load_data()

# print(    size(X_train_full)    ) # 153.600.000

X_valid, X_train = X_train_full[:5000] / 255., X_train_full[5000:] / 255.
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255.

model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[28, 28]),
    keras.layers.Dense(300, activation="relu"),
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

model.compile(loss="sparse_categorical_crossentropy",
              optimizer="sgd",
              metrics=["accuracy"])

history = model.fit(X_train, y_train, epochs=1,
                    validation_data=(X_valid, y_valid))
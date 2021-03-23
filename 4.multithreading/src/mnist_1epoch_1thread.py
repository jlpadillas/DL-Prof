#!/usr/bin/env python3
# coding: utf-8

# Primera prueba:
# vamos a aislar en un core a tensorflow, y vamos a medir con perf los eventos de dicho core.
# 
# vamos a hacer una ejecución corta de mnist.py, una sola época (puedes usar el código que ya
# tienes, mira a ver cómo se define el número de epochs), un solo thread (bajar intra e inter
# op parallelism a 1) y medir con perf.
# 
# Las stats que yo sacaría son: instrucciones totales, ciclos totales, instrucciones de punto
# flotante (ojo con estas, te va a tocar buscar cuales son de todas las disponibles en los 
# eventos!!).
# 
# Comando: perf -e XXXX -C <n> taskset -c <n>x mnist_1epoch_1thread.py
# -------------------------------------------------------------------------------------------

# TensorFlow ≥2.0 is required
import tensorflow as tf
assert tf.__version__ >= "2.0"

from tensorflow import keras

# Parallalism is set to 1
print(tf.config.threading.get_inter_op_parallelism_threads(), 
    tf.config.threading.get_intra_op_parallelism_threads())

tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)

print(tf.config.threading.get_inter_op_parallelism_threads(), 
    tf.config.threading.get_intra_op_parallelism_threads())

fashion_mnist = keras.datasets.fashion_mnist
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

X_valid, X_train = X_train_full[:5000] / 255., X_train_full[5000:] / 255.
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255.

# class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
#                "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

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

# model.evaluate(X_test, y_test)

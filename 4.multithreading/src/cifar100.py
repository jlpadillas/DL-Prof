#!/usr/bin/env python3
# coding: utf-8

# TensorFlow ≥2.0 is required
import os
import tensorflow as tf
assert tf.__version__ >= "2.0"

from tensorflow import keras

# Parallalism is set to 1
# print(tf.config.threading.get_inter_op_parallelism_threads(), 
#     tf.config.threading.get_intra_op_parallelism_threads())

# tf.config.threading.set_inter_op_parallelism_threads(1)
# tf.config.threading.set_intra_op_parallelism_threads(1)

# print(tf.config.threading.get_inter_op_parallelism_threads(), 
#     tf.config.threading.get_intra_op_parallelism_threads())

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))




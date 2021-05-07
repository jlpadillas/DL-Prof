#!/usr/bin/env python3
# coding: utf-8

# ------------------------------------------------------------------------ #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["University of Cantabria"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
if __name__ == "__main__":
    """
    TODO
    """

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
    # standard library

    # ! starts
    print("\nSTARTS MNIST...")


    import os
    import pathlib
    import sys

    # Forces the program to execute on CPU
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    # Just disables the warning, doesn't take advantage of AVX/FMA to run faster
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # -------------------------------------------------------------------- #
    # Params
    # -------------------------------------------------------------------- #
    # Current working directory (Makefile from)
    PWD = pathlib.Path(__file__).parent.parent.absolute()

    # Carpeta donde se encuentran los ejecutables
    BIN_DIR = PWD / "bin"
    # Carpeta donde se encuentran los archivos de configuracion
    CFG_DIR = PWD / "conf"
    # Carpeta donde se encuentran las librerias generadas
    LIB_DIR = PWD / "lib"
    # Carpeta donde se vuelcan los datos de salida
    OUT_DIR = PWD / "out"
    # Carpeta donde se encuentran los archivos fuente
    SRC_DIR = PWD / "src"

    # sys.path.append(str(PWD_MAT_MUL / SRC_DIR))
    from my_papi import my_papi
    # Se crea un objeto de la clase my_papi
    libname = LIB_DIR / "libmy_papi.so"
    mp = my_papi(libname)

    # -------------------------------------------------------------------- #
    # MY_PAPI
    # -------------------------------------------------------------------- #
    # events_file = CFG_DIR / "events_pc.cfg"
    events_file = CFG_DIR / "events_laptop.cfg"
    # events_file = CFG_DIR / "events_node.cfg"
    # -------------------------------------------------------------------- #
    cpus = list(range(0, int(mp.get_num_logical_cores())))
    mp.prepare_measure(str(events_file), cpus)
    # mp.prepare_measure(str(events_file), None)
    mp.start_measure()

    # -------------------------------------------------------------------- #
    # ROI
    # -------------------------------------------------------------------- #

    # TensorFlow ≥2.0 is required
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
    # -------------------------------------------------------------------- #
    # END ROI
    # -------------------------------------------------------------------- #
    mp.stop_measure()
    print("After stop")
    mp.print_results("out/FICH.csv")
    print("After print")
    # mp.end_measure()
    print("EOF")
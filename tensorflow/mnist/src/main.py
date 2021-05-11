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

    # standard library
    import os
    import pathlib

    # Forces the program to execute on CPU
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

    # Just disables the warning, doesn't take advantage of AVX/FMA to run faster
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # 3rd party packages

    # local source
    from my_papi import my_papi
    from my_callbacks import my_callbacks
    from mnist import mnist
    from format_results import format_results

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
    # -------------------------------------------------------------------- #

    # Se crea un objeto de la clase my_papi
    libname = LIB_DIR / "libmy_papi.so"
    mp = my_papi(libname)

    # Create an object mnist
    mnst = mnist()

    mnst.setup()

    mnst.set_parallelism(None, None)

    # -------------------------------------------------------------------- #
    # MY_PAPI
    # -------------------------------------------------------------------- #
    # events_file = CFG_DIR / "events_pc.cfg"
    # events_file = CFG_DIR / "events_laptop.cfg"
    # events_file = CFG_DIR / "events_node.cfg"
    events_file = CFG_DIR / "events_node_mnist.cfg"
    # -------------------------------------------------------------------- #

    cpus = list(range(0, int(mp.get_num_logical_cores())))

    mp.prepare_measure(str(events_file), cpus)

    batch_size = 128
    epoch = 1
    callbacks = [my_callbacks(path_to_lib=str(libname),
                              events_file=str(events_file))]
    # callbacks = None

    mp.start_measure()

    # -------------------------------------------------------------------- #
    # ROI
    # -------------------------------------------------------------------- #

    mnst.fit(my_batch_size=batch_size, my_epoch=epoch,
             my_callbacks=callbacks)

    # -------------------------------------------------------------------- #
    # END ROI
    # -------------------------------------------------------------------- #
    mp.stop_measure()

    output_file = "out/file.csv"
    mp.print_measure(output_file)

    mp.finalize_measure()

    # fm = format_results()
    # fm.create_dash_table(events_file, output_file)

    # mp.check_results(output_file)

    # mp.create_dash_table(output_file)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

    # Forces the program to execute on CPU
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

    # Just disables the warning, doesn't take advantage of AVX/FMA to run faster
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # 3rd party packages

    # local source
    from mnist import mnist

    # -------------------------------------------------------------------- #

    # Create an object mnist
    mnst = mnist()

    mnst.setup()

    # mnst.set_parallelism(None, None)

    # -------------------------------------------------------------------- #
    # ROI
    # -------------------------------------------------------------------- #

    mnst.fit()

    # -------------------------------------------------------------------- #
    # END ROI
    # -------------------------------------------------------------------- #

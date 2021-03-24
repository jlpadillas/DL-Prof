#! /usr/bin/env python3
# -- coding: utf-8 --

# standard library

# 3rd party packages
import numpy as np

# local source

# ------------------------------------------------------------------------ #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["Universidad de Cantabria"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #


class matrix(object):
    """Matrix class that allows performing different operations with 
    matrices of different dimensions."""

    # Attributes
    # dim_x     # Matrix dimension on x-axis
    # dim_y     # Matrix dimension on y-axis
    # M         # Matrix M
    # N         # Matrix N
    # A         # Matrix A = M * N

    def __init__(self, dim_x=None, dim_y=None):
        """Constructor."""
        super(matrix, self).__init__()
        if dim_x is None or dim_y is None:
            # Default values
            self.dim_x = 500
            self.dim_y = 500
            print("Using default values of dimension: dim_x = dim_y = 500")
        else:
            self.dim_x = dim_x
            self.dim_y = dim_y

    def empty_matrices(self):
        """Genera dos matrices M y N con la funcion empty() de Numpy y de
        tipo float."""
        self.M = np.empty([self.dim_x, self.dim_y], dtype=float)
        self.N = np.empty([self.dim_x, self.dim_y], dtype=float)

    def zeros_matrices(self):
        """Genera dos matrices M y N con la funcion zeros() de Numpy y de
        tipo float."""
        self.M = np.zeros([self.dim_x, self.dim_y], dtype=float)
        self.N = np.zeros([self.dim_x, self.dim_y], dtype=float)

    def sequential_matrices(self):
        self.M = np.arange(
            self.dim_x * self.dim_y).reshape(self.dim_x, self.dim_y)
        #TODO
        pass

    def random_matrices(self):
        # TODO
        pass

    def multiply(self):
        """Multiplica las dos matrices M y N mediante la funcion matmul()
        de Numpy."""
        if self.M is None or self.N is None:
            raise self.MatricesUndefinedError
        self.A = np.matmul(self.M, self.N)

    # -------------------------------------------------------------------- #
    # define Python user-defined exceptions

    class Error(Exception):
        """Base class for other exceptions"""
        pass

    class MatricesUndefinedError(Error):
        """Raised when the input values are less than two arguments."""
        pass
    # -------------------------------------------------------------------- #
# ------------------------------------------------------------------------ #

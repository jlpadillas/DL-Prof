#! /usr/bin/env python3
# -- coding: utf-8 --

# standard library

# 3rd party packages
import numpy as np

__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["Universidad de Cantabria"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# ------------------------------------------------------------------------ #

class matrix(object):
    """Clase matrix que permite realizar distintas operaciones con matrices
    de diferentes dimensiones."""

    # Attributes
    # dim_x
    # dim_y
    # M
    # N
    # A

    def __init__(self, dim_x=None, dim_y=None):
        """Constructor de la clase matrix."""
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


# ------------------------------------------------------------------------ #
if __name__ == "__main__":
    """Dependiendo del valor pasado por parametro, se ejecuta la multipli-
    cacion de dos matrices rellenadas con la funcion empty() o zeros(),
    ambas pertenecientes a la liberia Numpy.
    @param option variable que se pasa por parametro y que indica si se ha
        de rellenar las matrices con la funcion empty() o zeros().
    """
    # standard library
    import sys

    # 3rd party packages

    # Se lee el argumento pasado
    option = None
    if len(sys.argv) > 1:
        option = sys.argv[1]

    # Se usan matrices cuadradas para facilitar el calculo de operaciones.
    dim_x = 5000
    dim_y = dim_x

    # Se crea el objeto
    mat = matrix(dim_x, dim_y)
    # mat = matrix()

    # Se generan las dos matrices
    if option == "empty":
        mat.empty_matrices()
    elif option == "zeros":
        mat.zeros_matrices()
    else:
        print("ERROR: Wrong generation of matrices. Run the program with "
              "argument 'empty' or 'zeros'.")
        raise mat.Error

    # ROI -> Se multiplican
    mat.multiply()

    # print(M)
    # print(N)
    # print(A)

    ########################################################################
    #
    # Ejemplo de multiplicacion de matrices de tamanho 3x3:
    #
    # +-----+-----+-----+     +-----+-----+-----+
    # |  0  |  1  |  2  |     |  8  |  7  |  6  |
    # +-----+-----+-----+     +-----+-----+-----+
    # |  3  |  4  |  5  |  x  |  5  |  4  |  3  |  =
    # +-----+-----+-----+     +-----+-----+-----+
    # |  6  |  7  |  8  |     |  2  |  1  |  0  |
    # +-----+-----+-----+     +-----+-----+-----+
    #
    #   +-------------------+-------------------+-------------------+
    #   |  0*8 + 1*5 + 2*2  |  0*7 + 1*4 + 2*1  |  0*6 + 1*3 + 2*0  |
    #   +-------------------+-------------------+-------------------+
    #   |  3*8 + 4*5 + 5*2  |  3*7 + 4*4 + 5*1  |  3*6 + 4*3 + 5*0  |  =
    #   +-------------------+-------------------+-------------------+
    #   |  6*8 + 7*5 + 8*2  |  6*7 + 7*4 + 8*1  |  6*6 + 7*3 + 8*0  |
    #   +-------------------+-------------------+-------------------+
    #
    #       +------+------+------+
    #       |   9  |   6  |   3  |
    #       +------+------+------+
    #       |  54  |   1  |   2  |
    #       +------+------+------+
    #       |  99  |  78  |  57  |
    #       +------+------+------+
    #
    # Así, si tenemos matrices cuadradas de nxn, entonces el número de
    # multiplicaciones es igual a n**3.
    #
    ########################################################################

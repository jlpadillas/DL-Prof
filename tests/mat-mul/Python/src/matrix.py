#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
import random
import sys
import threading

# 3rd party packages

# local source

# --------------------------------------------------------------------------- #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["University of Cantabria", "Pablo Abad", "Pablo Prieto"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #


class matrix(object):
    """
    A class used to represent a Matrix and perform different operations with
    matrices of different dimensions.

    Attributes
    ----------
    rows_default : int
        default value of rows for generate a matrix
    cols_default : int
        default value of cols for generate a matrix

    Methods
    -------
    init_empty(rows=None, cols=None)
        desc
    init_random(rows=None, cols=None)
        desc
    init_seq(rows=None, cols=None)
        desc
    init_zeros(rows=None, cols=None)
        desc
    mat_mul(M_a=None, M_b=None)
        desc
    """

    # Attributes
    # self.MAX_RANDOM
    # self.NUM_THREADS

    def __init__(self):
        """Constructor."""

        super(matrix, self).__init__()

        # Attributes
        self.MAX_RANDOM = 10
        self.NUM_THREADS = 16

        # Establish the warning format
        # warnings.formatwarning = self.__warning_on_one_line

    # -------------------------------------------------------------------- #

    def print_matrix(self, M):
        """Returns a Numpy matrix initialized with the function empty().

        If the arguments `rows` or `cols` aren't passed in, the default
        attributes are used.

        Parameters
        ----------
        rows : int, optional
            The number of rows of the matrix (default is None)
        
        cols : int, optional
            The number of cols of the matrix (default is None)

        Returns
        -------
        numpy.matrix
            a floating point matrix of size rows x cols.

        Raises
        ------
        ValueError
            If the arguments passed in are not positive.
        """

        rows = len(M)
        cols = len(M[-1])

        mat_str = "\n"
        for i in range(rows):
            mat_str += "|\t"
            for j in range(cols):
                mat_str += str(M[i][j]) + "\t"
                if j == cols - 1:
                    mat_str += "|\n"
        print(mat_str)
    # -------------------------------------------------------------------- #

    def init_rand(self, rows, cols):
        """Returns a Numpy matrix with its values randomly initialized.

        If the arguments `rows` or `cols` aren't passed in, the default
        attributes are used.

        Parameters
        ----------
        rows : int, optional
            The number of rows of the matrix (default is None)
        
        cols : int, optional
            The number of cols of the matrix (default is None)

        Returns
        -------
        numpy.matrix
            a floating point matrix of size rows x cols.

        Raises
        ------
        ValueError
            If the arguments passed in are not positive.
        """

        M = []
        for r in range(rows):
            arr = []
            for c in range(cols):
                arr.append(float(random.randrange(self.MAX_RANDOM)))
            M.append(arr)

        return M
    # -------------------------------------------------------------------- #

    def init_seq(self, rows, cols):
        """Returns a Numpy matrix with its values sequentially initialized.

        If the arguments `rows` or `cols` aren't passed in, the default
        attributes are used.

        Parameters
        ----------
        rows : int, optional
            The number of rows of the matrix (default is None)
        
        cols : int, optional
            The number of cols of the matrix (default is None)

        Returns
        -------
        matrix
            a floating point matrix of size rows x cols.

        """

        M = []
        for r in range(rows):
            arr = []
            for c in range(cols):
                arr.append(float(r * cols + c))
            M.append(arr)

        return M
    # -------------------------------------------------------------------- #

    def mat_mul(self, M_a, M_b):
        """Returns a Numpy matrix product of a multiplication of matrices.

        If the arguments `M_a` or `M_a` aren't passed in, the operation
        cannot be performed.

        Parameters
        ----------
        M_a : numpy.matrix
            A matrix, first term of the multiplication (default is None)
        
        M_b : numpy.matrix
            A matrix, second term of the multiplication (default is None)

        Returns
        -------
        numpy.matrix
            a floating point matrix.

        Raises
        ------
        MatricesUndefinedError
            If there is no argument passed.
        """

        rows_a = len(M_a)
        cols_a = len(M_a[-1])
        rows_b = len(M_b)
        cols_b = len(M_b[-1])

        if cols_a != rows_b:
            print("[ERROR] #columns A must be equal to #rows B.\n")
            sys.exit(-1)

        M_c = []
        for i in range(rows_a):
            arr = []
            for k in range(cols_b):
                sum = 0.0
                for j in range(cols_a):
                    sum += float(M_a[i][j]) * float(M_b[j][k])
                arr.append(sum)
            M_c.append(arr)
        return M_c
    # -------------------------------------------------------------------- #

    def mat_mul_transpose(self, M_a, M_b):
        """Returns a Numpy matrix product of a multiplication of matrices.

        If the arguments `M_a` or `M_a` aren't passed in, the operation
        cannot be performed.

        Parameters
        ----------
        M_a : numpy.matrix
            A matrix, first term of the multiplication (default is None)
        
        M_b : numpy.matrix
            A matrix, second term of the multiplication (default is None)

        Returns
        -------
        numpy.matrix
            a floating point matrix.

        Raises
        ------
        MatricesUndefinedError
            If there is no argument passed.
        """

        rows_a = len(M_a)
        cols_a = len(M_a[-1])
        rows_b = len(M_b)
        cols_b = len(M_b[-1])

        if cols_a != rows_b:
            print("[ERROR] #columns A must be equal to #rows B.\n")
            sys.exit(-1)

        # Calculate the transpose
        M_b_Tr = []
        for i in range(rows_b):
            arr = []
            for j in range(cols_b):
                arr.append(M_b[j][i])
            M_b_Tr.append(arr)

        M_c = []
        for i in range(rows_a):
            arr = []
            for k in range(cols_b):
                sum = 0.0
                for j in range(cols_a):
                    sum += float(M_a[i][j]) * float(M_b_Tr[k][j])
                arr.append(sum)
            M_c.append(arr)
        return M_c
    # -------------------------------------------------------------------- #

    def __multi(self, M_a, M_b, M_c, cols_c, rows_c):
        cols_a = len(M_a[-1])

        aux = []
        for i in range(rows_c[0], rows_c[1]):
            arr = []
            for k in range(cols_c[0], cols_c[1]):
                sum = 0.0
                for j in range(cols_a):
                    sum += float(M_a[i][j]) * float(M_b[j][k])
                arr.append(sum)
            aux.append(arr)

        # Store the values in the result matrix
        i = 0
        for j in range(rows_c[0], rows_c[1]):
            M_c[j] = aux[i]
            i += 1
    # -------------------------------------------------------------------- #

    def mat_mul_multithread(self, M_a, M_b):

        # NUM_THREADS = 2
        rows_a = len(M_a)
        cols_a = len(M_a[-1])
        rows_b = len(M_b)
        cols_b = len(M_b[-1])

        if cols_a != rows_b:
            print("[ERROR] #columns A must be equal to #rows B.\n")
            sys.exit(-1)

        rows_per_thread = int(rows_a / self.NUM_THREADS)
        rest_of_matrix = rows_a % self.NUM_THREADS

        M_c = [[0] * cols_b] * rows_a

        # Create and start the threads
        threads = []
        for i in range(self.NUM_THREADS):
            # Calculate the params to pass them to the thread
            # TODO: The last thread operates the rest. Modify in a future and
            # TODO: let the first thread to end, operate the rest.
            cols_c_start = 0
            cols_c_end = cols_b
            rows_c_start = rows_per_thread * i
            rows_c_end = rows_c_start + rows_per_thread

            if (i == self.NUM_THREADS - 1) and (rest_of_matrix != 0):
                rows_c_end += rest_of_matrix

            cols_c = [cols_c_start, cols_c_end]
            rows_c = [rows_c_start, rows_c_end]

            t = threading.Thread(target=self.__multi, args=(M_a, M_b, M_c, cols_c, rows_c,))
            threads.append(t)
            t.start()

        # Join the threads
        for t in threads:
            t.join()

        return M_c
    # -------------------------------------------------------------------- #


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

#! /usr/bin/env python3
# -- coding: utf-8 --

# standard library
import warnings

# 3rd party packages
import numpy as np

# local source

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
    rows_default = 500
    cols_default = 500

    def __init__(self):
        """Constructor."""

        super(matrix, self).__init__()

        # Establish the warning format
        warnings.formatwarning = self.__warning_on_one_line

    # -------------------------------------------------------------------- #

    def init_empty(self, rows=None, cols=None):
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

        # If none dimension is passed, it just use the default ones
        if rows is None or cols is None:
            message = "No dimensions introduced, using cols=" + \
                str(self.rows_default) + " and rows=" + \
                str(self.cols_default) + "."
            warnings.warn(message, Warning)
            rows = self.rows_default
            cols = self.cols_default
        elif rows < 0 or cols < 0:
            raise ValueError

        return np.empty([rows, cols], dtype=float)
    # -------------------------------------------------------------------- #

    def init_rand(self, rows=None, cols=None):
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

        # If none dimension is passed, it just use the default ones
        if rows is None or cols is None:
            message = "No dimensions introduced, using cols=" + \
                str(self.rows_default) + " and rows=" + \
                str(self.cols_default) + "."
            warnings.warn(message, Warning)
            rows = self.rows_default
            cols = self.cols_default
        elif rows < 0 or cols < 0:
            raise ValueError

        return np.random.rand(rows, cols)
    # -------------------------------------------------------------------- #

    def init_seq(self, rows=None, cols=None):
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
        numpy.matrix
            a floating point matrix of size rows x cols.

        Raises
        ------
        ValueError
            If the arguments passed in are not positive.
        """

        # If none dimension is passed, it just use the default ones
        if rows is None or cols is None:
            message = "No dimensions introduced, using cols=" + \
                str(self.rows_default) + " and rows=" + \
                str(self.cols_default) + "."
            warnings.warn(message, Warning)
            rows = self.rows_default
            cols = self.cols_default
        elif rows < 0 or cols < 0:
            raise ValueError

        return np.arange(cols * rows, dtype=float).reshape(cols, rows)
    # -------------------------------------------------------------------- #

    def init_zeros(self, rows=None, cols=None):
        """Returns a Numpy matrix initialized with the function zeros().

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

        # If none dimension is passed, it just use the default ones
        if rows is None or cols is None:
            message = "No dimensions introduced, using cols=" + \
                str(self.rows_default) + " and rows=" + \
                str(self.cols_default) + "."
            warnings.warn(message, Warning)
            rows = self.rows_default
            cols = self.cols_default
        elif rows < 0 or cols < 0:
            raise ValueError

        return np.zeros([rows, cols], dtype=float)
    # -------------------------------------------------------------------- #

    def mat_mul(self, M_a=None, M_b=None):
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

        if M_a is None or M_b is None:
            raise self.MatricesUndefinedError
        return np.matmul(M_a, M_b)
    # -------------------------------------------------------------------- #

    def __warning_on_one_line(self, message, category, filename, lineno,
                              file=None, line=None):
        """Format the warning output."""

        return '%s:%s:\n\t%s: %s\n' % (filename, lineno, category.__name__,
                                       message)
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

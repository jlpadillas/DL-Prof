#! /usr/bin/env python3
# -- coding: utf-8 --

# standard library

# 3rd party packages
import numpy as np

# ------------------------------------------------------------------------ #
# Multiplicacion de dos matrices: A = M  N usando numpy

__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["Universidad de Cantabria"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"


dim_x = 5000
dim_y = dim_x

# Genera las matrices random
# M = np.random.rand(dim_x, dim_y)
# N = np.random.rand(dim_x, dim_y)

# Genera las matrices "controladas"
M = np.empty([dim_x, dim_y], dtype=float)
N = np.empty([dim_x, dim_y], dtype=float)
# M, N = np.mgrid[0.0:dim_x,0.0:dim_y]

# ROI
A = np.matmul(M, N)
# print(M)
# print(N)
# print(A)

#############
#
# Ejemplo de multiplicacion de matrices de tamanho 3x3:
#
# +-----+-----+-----+     +-----+-----+-----+     +-------------------+-------------------+-------------------+     +------+------+------+
# |  0  |  1  |  2  |     |  8  |  7  |  6  |     |  0*8 + 1*5 + 2*2  |  0*7 + 1*4 + 2*1  |  0*6 + 1*3 + 2*0  |     |   9  |   6  |   3  |
# +-----+-----+-----+     +-----+-----+-----+     +-------------------+-------------------+-------------------+     +------+------+------+
# |  3  |  4  |  5  |  x  |  5  |  4  |  3  |  =  |  3*8 + 4*5 + 5*2  |  3*7 + 4*4 + 5*1  |  3*6 + 4*3 + 5*0  |  =  |  54  |   1  |   2  |
# +-----+-----+-----+     +-----+-----+-----+     +-------------------+-------------------+-------------------+     +------+------+------+
# |  6  |  7  |  8  |     |  2  |  1  |  0  |     |  6*8 + 7*5 + 8*2  |  6*7 + 7*4 + 8*1  |  6*6 + 7*3 + 8*0  |     |  99  |  78  |  57  |
# +-----+-----+-----+     +-----+-----+-----+     +-------------------+-------------------+-------------------+     +------+------+------+
#
# Así, si tenemos matrices cuadradas, nxn, entonces el número de multiplicaciones es igual a n**3
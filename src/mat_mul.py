#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library

# 3rd party packages
import numpy as np

# ------------------------------------------------------------------------ #
# Multiplicacion de dos matrices: A = M * N usando numpy

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

M = np.random.rand(dim_x, dim_y)
N = np.random.rand(dim_x, dim_y)

# ROI
A = np.matmul(M, N)

# print(M, N, A)

#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
from time import time

# 3rd party packages
import numpy as np
import measure

__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2020"
__credits__ = "Universidad de Cantabria"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"

# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
    """Programa principal"""

    # Start time
    tiempo_inicial = time()

    # ------------------------------------------------------------------------ #
    m = measure()

    m.perf_stat
    # br = Branch("branch.cpp")
    # print(br.get_branch_cambio())
    # br = Branch("branch_cambio.cpp")
    # print(br.get_branch_cambio())
    # ------------------------------------------------------------------------ #

    # End time
    tiempo_final = time()
    hours, rem = divmod(tiempo_final - tiempo_inicial, 3600)
    minutes, seconds = divmod(rem, 60)
    print(" > Execution time: {:0>2}:{:0>2}:{:05.4f}".format(
        int(hours), int(minutes), seconds))
# ---------------------------------------------------------------------------- #
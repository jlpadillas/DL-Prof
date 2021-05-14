#! /usr/bin/env python3
# -- coding: utf-8 --

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
    """Dependiendo del valor pasado por parametro, se ejecuta la multipli-
    cacion de dos matrices rellenadas con la funcion empty() o zeros(),
    ambas pertenecientes a la liberia Numpy.
    @param option variable que se pasa por parametro y que indica si se ha
        de rellenar las matrices con la funcion empty() o zeros().
    """

    # standard library
    import sys
    import locale

    # 3rd party packages

    # local source
    from matrix import matrix

    # Define the locale format
    locale.setlocale(locale.LC_ALL, '')

    # Se lee el argumento pasado
    option = None
    if len(sys.argv) > 1:
        option = sys.argv[1]

    # Se usan matrices cuadradas para facilitar el calculo de operaciones.
    dim_x = 1000
    dim_y = dim_x

    # Se crea el objeto
    mat = matrix()
    # mat = matrix()

    # Se generan las dos matrices
    if option == "empty":
        M = mat.init_empty(rows=dim_x, cols=dim_y)
        N = mat.init_empty(rows=dim_x, cols=dim_y)
    elif option == "zeros":
        M = mat.init_zeros(rows=dim_x, cols=dim_y)
        N = mat.init_zeros(rows=dim_x, cols=dim_y)
    elif option == "seq":
        M = mat.init_seq(rows=dim_x, cols=dim_y)
        N = mat.init_seq(rows=dim_x, cols=dim_y)
    elif option == "rand":
        M = mat.init_rand(rows=dim_x, cols=dim_y)
        N = mat.init_rand(rows=dim_x, cols=dim_y)
    else:
        print("ERROR: Wrong generation of matrices. Run the program with "
              "argument 'empty', 'zeros', 'seq' or 'rand'.")
        raise mat.Error

    # ROI -> Se multiplican
    mat.mat_mul(M, N)

    # print(M)
    # print(N)
    # print(A)

    if dim_x == dim_y:
        num = (dim_x * dim_x) * (2 * dim_x - 1)
        print("\n FP operations expected (aprox.): " +
              locale.format_string('%.0f', num, grouping=True))

    ########################################################################
    #
    # Ejemplo de multiplicacion de matrices de tamanho 3x3:
    #
    # +-----+-----+-----+     +-----+-----+-----+
    # |  0  |  1  |  2  |     |  8  |  7  |  6  |
    # +-----+-----+-----+     +-----+-----+-----+
    # |  3  |  4  |  5  |  *  |  5  |  4  |  3  |  =
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
    # Sin embargo, hay que tener en cuenta las sumas que, también, son
    # medidas. Así, la ecuación a utilizar es: n**2(2n-1)
    #
    ########################################################################
# ------------------------------------------------------------------------ #

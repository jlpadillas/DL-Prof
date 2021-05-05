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
    import pathlib

    # 3rd party packages

    # local source
    from matrix import matrix
    from my_papi import my_papi

    # Define the locale format
    locale.setlocale(locale.LC_ALL, '')

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

    # Hay que hacer append del path del src para que encuentre ficheros
    sys.path.append(SRC_DIR)

    # Se crea un objeto de la clase my_papi
    libname = LIB_DIR / "libmy_papi.so"
    mp = my_papi(libname)

    # -------------------------------------------------------------------- #
    events_file = CFG_DIR / "events_pc.cfg"
    # events_file = CFG_DIR / "events_laptop.cfg"
    # events_file = CFG_DIR / "events_node.cfg"

    # -------------------------------------------------------------------- #
    # Execution
    # -------------------------------------------------------------------- #
    cpus = mp.get_cores()
    mp.prepare_measure(str(events_file), cpus)
    mp.start_measure()

    # -------------------------------------------------------------------- #
        # Se lee el argumento pasado
    option = None
    if len(sys.argv) > 1:
        option = sys.argv[1]

    # Se usan matrices cuadradas para facilitar el calculo de operaciones.
    dim_x = 6000
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
    # -------------------------------------------------------------------- #

    mp.stop_measure()
    mp.print_measure(file_name="out/comida.csv")
    mp.end_measure()



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

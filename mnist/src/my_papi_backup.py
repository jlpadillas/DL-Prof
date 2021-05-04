#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
import locale
import warnings

# 3rd party packages
from ctypes import *

# local source
from system_setup import system_setup

# --------------------------------------------------------------------------- #
__author__ = "Juan Luis Padilla Salomé"
__copyright__ = "Copyright 2021"
__credits__ = ["Universidad de Cantabria", "Pablo Abad", "Pablo Prieto"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé"
__email__ = "juan-luis.padilla@alumnos.unican.es"
__status__ = "Production"
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #


class my_papi(system_setup):
    """Permite realizar medidas de los eventos mediante el uso de la 
    libreria libmy_papi.so, que a su vez se basa en el codigo de PAPI."""

    # Attributes
    # ----------
    # self.cores = [] # Array de cores logicos pertenecientes al mismo fisico
    default_events = ["cycles", "instructions"]
    # self.p_lib = CDLL # Con el se puede acceder a la liberia y sus func.
    # self.events = []  # Eventos a ser medidos
    # selg.values = []  # lista con los valores medidos

    # self. ptr_EventSets # Puntero que indica la loc. en mem. del eventSet

    def __init__(self, path):
        """Constructor de la clase my_papi que recibe por parametro la 
        localizacion de la liberia libmy_papi.so."""

        super(my_papi, self).__init__()

        # Loads the library path
        self.__set_my_lib(path)

        # Establish the warning format
        warnings.formatwarning = self.__warning_on_one_line
    # ----------------------------------------------------------------------- #

    def start_measure(self, events=None, cpus=None):
        """Gets the events to be measured and starts it."""

        # If none events is passed, it just measures the default events.
        if events is None:
            warnings.warn("No input events, measuring defaults!", Warning)
            events = self.default_events

        # Stores the values in attributes
        self.events = events
        self.cpus = cpus

        # ------------------------------------------------------------------- #
        # Convert the EVENTS to pass them to the functions on C
        # TODO: Change this
        # events_bytes = []
        # for i in range(len(events)):
        #     events_bytes.append(bytes(events[i], 'utf-8'))

        # # Se crea un array con los eventos a pasar
        # events = (c_char_p * (len(events_bytes) + 1))()

        # # Take all items except the last one
        # events[:-1] = events_bytes
        events_bytes = []
        for i in range(len(events)):
            events_bytes.append(bytes(events[i], 'utf-8'))

        # Se crea un array con los eventos a pasar
        events_array = (c_char_p * (len(events_bytes) + 1))()

        # Corta el string para eliminar el last char = \n
        events_array[:-1] = events_bytes
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # Converts the CPUS to pass them to the functions on C
        if cpus is not None:
            cpus = (c_int * len(cpus))(*cpus)
        # Ctypes uses None as NULL in C
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # Params for the functions
        # ------------------------------------------------------------------- #
        num_events = c_int(len(events))
        event_set = c_int()
        num_event_set = c_int(1)

        # Depends if the measure is on multiples cpus or not
        if cpus is None or len(cpus) < 2:
            # Call the C function my_configure_eventSet(...)
            self.p_lib.my_configure_eventSet(byref(event_set))
        else:
            num_cpus = c_int(len(cpus))
            # Call the function my_attach_cpus(...)
            self.p_lib.my_attach_cpus(num_cpus, cpus, byref(event_set))
            num_event_set = c_int(len(cpus))

        # We need to modify the definition of second argument
        self.p_lib.my_start_events.argtypes = [c_int, c_char_p * len(events_array),
                                               POINTER(c_int), c_int]

        # Call the function my_start_events(...)
        self.p_lib.my_start_events(
            num_events, events_array, byref(event_set), num_event_set)

        # Store important parameters
        self.event_set = event_set

        #     # --------------------------------------------------------------- #
        #     # int my_attach_cpus(int num_cpus, const int cpus[],
        #     #                    int *eventSets)
        #     my_attach_cpus = self.p_lib.my_attach_cpus
        #     my_cpus = c_int * len(cpus)
        #     my_attach_cpus.argtypes = [c_int, my_cpus, POINTER(c_int)]
        #     my_attach_cpus.restype = c_int
        #     # --------------------------------------------------------------- #
        #     num_event_set = len(cpus)
        #     my_attach_cpus(num_event_set, my_cpus, byref(self.event_set))
        # # ------------------------------------------------------------------- #
        # # ! Se prepara las funciones para llamar al stop
        # self.values = (c_longlong * len(self.events))()
        # self.ptr_EventSets

        # # Empieza la medida de los eventos para multithreading
        # # TODO: editar?
        # self.ptr_EventSet = self.p_lib.my_start_events(
        #     events_array, len(self.events))
    # ----------------------------------------------------------------------- #

    def stop_measure(self):
        """Detiene la lectura de datos y guarda los valores obtenidos."""

        # Se definen los parametros de entrada y salida de la funcion C
        # self.p_lib.my_stop_events.argtypes = c_int, c_int, POINTER(c_longlong)
        res_measure = (POINTER(c_longlong * len(self.events)))()
        # res_all = POINTER()
        # self.p_lib.my_stop_events.argtypes = [c_int, POINTER(c_int), c_int,
        #                                 # POINTER(POINTER(c_longlong))]
        #                                 res_measure]
        # self.p_lib.my_stop_events.restype = c_int

        # Se guarda espacio en memoria y se leen los resultados
        # Reserve space in memory
        # long long **m_values = (long long **)my_malloc(num_cpus *
        #                                        sizeof(long long *));

        # Allocate memory for the pointers of cpus
        # if self.cpus is None or len(self.cpus) == 0:
        #     # One pointer for one cpu
        #     self.events = (c_longlong)()
        # else:
        #     # As much as # of cpus we are measuring
        #     self.events = (c_longlong * len(self.cpus))()

        # Defining the common params to pass the function
        num_events = c_int(len(self.events))
        self.values = POINTER(c_longlong)()
        # self.values = POINTER(POINTER(c_longlong))
        event_set = self.event_set
        # And now, depending on the type of measure, we fill the params
        if self.cpus is None or len(self.cpus) == 0:
            num_event_set = c_int(1)
        else:
            num_event_set = c_int(len(self.cpus))

        # Call the function "my_stop_events(...)"
        self.p_lib.my_stop_events(num_events, event_set, num_event_set, # self.values)
                                #   byref(self.values))
                                res_measure)

        print("Comida", res_measure)

        # Stores the result
        # self.values = byref(values)

        # if self.cpus is None:
        #     # If the cpus is None, then we have to measure only one core

        #     self.values = self.p_lib.my_malloc()

        # else:
        #     # If the number of cups is not None, then we have a multithreaded
        #     # measure, and we need to use a double pointer for the results

        # self.values = self.p_lib.my_malloc()
        # self.values = (c_longlong * len(self.events))()
        # self.p_lib.my_stop_events(
        #     self.ptr_EventSet, len(self.events), self.values)

        # self.set_perf_event_paranoid()  # Default perf
    # ----------------------------------------------------------------------- #

    def get_results(self, format=dict):
        """
        Return the results in a specific format.
            @param: format dict or list
            @return string with the results
        """

        # Check if the results are formated
        try:
            self.values_list and self.values_dict
        except AttributeError:
            self.__format_values()

        # Returns the value
        if format is dict:
            return self.values_dict
        elif format is list:
            return self.values_list
    # ----------------------------------------------------------------------- #

    def print_results(self, format=dict):
        """
        Print the results in a specific format.
            @param: format dict or list
            @return string with the results
        """

        # Check if the results are formated
        try:
            self.values_list and self.values_dict
        except AttributeError:
            self.__format_values()

        # Sets the locale for prints
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

        # Printing with a specific format
        if format is dict:
            # Header
            print("{:>20}\t\t{:<}".format('Value', 'Event'))
            for event, value in self.values_dict.items():
                # Items
                print("{:>20,}\t\t{:<}".format(value, event).replace(',', '.'))
                # print("{:>20}\t\t{:<}".format(
                #     locale.format_string('%.0f', value, grouping=True), event))

        elif format is list:
            print(*self.values_list, sep="\t")
            # for v in self.values_list:
            #     print("{:>20}".format(locale.format_string('%.0f', v, grouping=True)))
    # ----------------------------------------------------------------------- #

    def free(self, ptr):
        """Frees memory of a pointer passed by parameter."""

        # Defining input/output parameters of function:
        # void my_free(void *ptr)
        my_free = self.p_lib.my_free
        my_free.argtypes = [POINTER(c_int)]
        my_free.restype = None

        # calling the function (casting int -> pointer to int)
        my_free(cast(ptr, POINTER(c_int)))

    def malloc(self, size):
        """Performs a reserver of memory of a size passed by parameter 
        (which) has to be an integer and positive (gt 0). The value return
        is of type c_void_p (pointer to void)."""

        # size must be an integer positive
        if (not isinstance(size, int)) or (size < 0):
            raise self.WrongParameterError

        # Defining input/output parameters of function:
        # void *my_malloc(size_t size)
        my_malloc = self.p_lib.my_malloc
        my_malloc.argtypes = [c_size_t]
        my_malloc.restype = c_void_p

        # Creating a param of type "c_size_t" with the value of arg. size
        size_param = c_size_t(size)

        # return call of c
        return my_malloc(size_param)

    def __format_values(self):
        """Transform the results obtanied as an array and as a dictionary"""

        # Check if the measure has been done/finished
        try:
            self.values
        except AttributeError:
            raise self.NoMeasureFinishedError

        # List
        self.values_list = list(self.values)

        # Dictionary
        self.values_dict = {}
        for i in range(len(self.events)):
            self.values_dict[self.events[i]] = self.values[i]
    # ----------------------------------------------------------------------- #

    def __load_functions(self):
        """Creates the main functions that may be used for the user."""

        # ------------------------------------------------------------------- #
        # int my_attach_cpus(int num_cpus, const int cpus[], int *eventSets)
        # ------------------------------------------------------------------- #
        self.p_lib.my_attach_cpus.argtypes = [c_int, c_int, POINTER(c_int)]
        self.p_lib.my_attach_cpus.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_configure_eventSet(int *eventSet)
        # ------------------------------------------------------------------- #
        self.p_lib.my_configure_eventSet.argtypes = [POINTER(c_int)]
        self.p_lib.my_configure_eventSet.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # void my_free(void *ptr)
        # ------------------------------------------------------------------- #
        self.p_lib.my_free.argtypes = [c_void_p]
        self.p_lib.my_free.restype = None
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # void *my_malloc(size_t size)
        # ------------------------------------------------------------------- #
        self.p_lib.my_malloc.argtypes = [c_size_t]
        self.p_lib.my_malloc.restype = c_void_p
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # void my_print_values(int num_events, const char *events[],
        #                      int num_cpus, const int cpus[],
        #                      long long **values)
        # ------------------------------------------------------------------- #
        self.p_lib.my_print_values.argtypes = [c_int, c_char_p, c_int, c_int,
                                               POINTER(POINTER(c_longlong))]
        self.p_lib.my_print_values.restype = None
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_start_events(int num_events, const char *events[],
        #                     int *eventSets, int num_eventSets);
        # ------------------------------------------------------------------- #
        # self.p_lib.my_start_events.argtypes = [c_int, c_char_p, POINTER(c_int),
        #                                        c_int]
        self.p_lib.my_start_events.restype = c_int
        # ------------------------------------------------------------------- #

        # ------------------------------------------------------------------- #
        # int my_stop_events(int num_events, int *eventSets, int num_eventSets,
        #                    long long **values)
        # ------------------------------------------------------------------- #
        # self.p_lib.my_stop_events.argtypes = [c_int, POINTER(c_int), c_int,
        #                                       POINTER(POINTER(c_longlong))]
        self.p_lib.my_stop_events.restype = c_int
        # ------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #

    def __set_my_lib(self, libname):
        """Carga la libreria de libmy_papi.so, para ello es necesario 
        indicar su PATH."""

        # Load the shared library into ctypes
        print(libname)
        self.p_lib = CDLL(libname)
        self.__load_functions()
    # ----------------------------------------------------------------------- #

    def __warning_on_one_line(self, message, category, filename, lineno,
                              file=None, line=None):
        """Format the warning output."""

        return '%s:%s:\n\t%s: %s\n' % (filename, lineno, category.__name__,
                                       message)
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    # define Python user-defined exceptions

    class Error(Exception):
        """Base class for other exceptions"""
        pass

    class NoMeasureFinishedError(Error):
        """Raised when there is no result obtained."""
        pass

    class WrongParameterError(Error):
        """Raised when there is an incorrect parameter."""
        pass
    # ----------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #

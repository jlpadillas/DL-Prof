#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# standard library
import os
import subprocess
import sys
from pathlib import Path
from subprocess import run

# 3rd party packages

# local source
from system_setup import system_setup

__author__ = "Juan Luis Padilla Salomé", "Daniel Fernández Castillo"
__copyright__ = "Copyright 2020"
__credits__ = ["Universidad de Cantabria", "Pablo Abad"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Juan Luis Padilla Salomé", "Daniel Fernández Castillo"
__email__ = "juan-luis.padilla@alumnos.unican.es",
"daniel.fernandezcas@alumnos.unican.es"
__status__ = "Production"


class perf_measure(system_setup):
    """Objeto que permite crear medidas con el comando perf. Analiza y trata los
    resultados obtenidos."""

    # --- Attributes --- #
    # self.cores = [] # Array de cores logicos pertenecientes al mismo fisico
    field_separator = ";"
    num_reps = 30  # Repeticiones de medida
    # Lugares donde se guardan los archivos
    SRCDIR = "src"
    BINDIR = "bin"
    RESDIR = "results"

    def __init__(self):
        """Constructor de la clase perf_measure."""
        super(perf_measure, self).__init__()
    # ------------------------------------------------------------------------ #

    def compile(self, file):
        """Compila el fichero pasado por parametro. El fichero ha de estar en la
        carpeta asociada a SRCDIR. Los formatos permitidos son de archivos C y
        C++."""

        path_to_file = os.path.join(self.SRCDIR, file)
        if not Path(path_to_file).is_file():
            sys.exit("> No existe el fichero a compilar.")

        # El ejecutable se llama igual que el fichero
        self.exec_name, file_extension = os.path.splitext(file)

        if file_extension == ".c":
            cc, parameters = "gcc", "-O0"
        elif file_extension == ".cpp":
            cc, parameters = "g++", "-std=c++11"
        else:
            sys.exit("> Extension del fichero no soportada.")

        self.path_to_bin = os.path.join(self.BINDIR, self.exec_name)
        run([cc, parameters, path_to_file, "-o", self.path_to_bin])
    # ------------------------------------------------------------------------ #

    def perf_stat(self, events, program, params=None):
        """Ejecuta el comando perf stat en la terminal y se registran los
        eventos. Los datos se devuelven en un array donde cada linea pertenece
        a un evento registrado. Cada entrada es un String y ha de ser procesada.
        eventos, y los valores son las medidas en un array.
        @param events eventos que se han de medir. Array de Strings.
                i.e.: ["instructions", "cycles", ...]
        @param program programa a ajecutar.
        @param params parametros necesarios para que se ejecute el programa.
        """

        cores = ','.join([str(x) for x in self.cores])
        events_with_comma = ",".join(events)  # Eventos separados con coma

        command = ["taskset", "-c", cores, "sudo", "perf", "stat",
                   "--event", events_with_comma,
                   "--repeat", str(self.num_reps),
                   "--field-separator", self.field_separator,
                   program]
        for j in params.split():
            command.append(j)

        # Habilita lectura de contadores
        self.enable_nmi_watchdog(enable=False)
        # Se ejecuta el comando
        execution = run(command, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, encoding="utf-8")
        self.enable_nmi_watchdog(enable=True)  # Deshabilita lectura de cont.
        # Se guarda cada medida del evento en un array. Todos ellos en otro arr
        aux = []
        for entry in execution.stdout.split("\n"):
            if entry is "":
                continue
            aux.append(entry.split(self.field_separator))

        return aux  # [[], [], ..., []]
    # ------------------------------------------------------------------------ #

    def perf_stat_dict(self, events, program, params=None):
        """Devuelve un array con diccionarios, donde hay tantos diccionarios
        como medidas."""
        array_of_dictionaries = []
        data = self.perf_stat(events, program, params)

        for medida in data:
            dictionary = {"Value": None, "Error (%)": None, "Unit": None}
            aux = self._string_to_float(medida[0])
            dictionary["Value"] = int(aux) if aux.is_integer() else aux
            dictionary["Unit"] = medida[1]
            dictionary["Event"] = medida[2]
            dictionary["Error (%)"] = self._string_to_float(medida[3])
            array_of_dictionaries.append(dictionary)

        return array_of_dictionaries  # [{}, {}, ..., {}]
    # ------------------------------------------------------------------------ #

    def _string_to_float(self, text):
        """Hace la conversion de una cadena de texto a float. Hace un cambio de
        formato, reemplazando las comas por puntos. Elimina el porcentaje y el
        separador de miles."""
        var = text.replace('%', '').replace('.', '').replace(',', '.')
        return float(var)
    # ------------------------------------------------------------------------ #

    def get_data(self, result):
        """A partir de un fichero csv de perf, obtiene las medidas realizadas"""
        # Se abre el fichero y se guardan las lineas en un array
        data = []
        file = open(result, "r")
        for line in file:
            aux = self.get_data_from_line(line)
            if aux != None:
                data.append(aux)

        return data
    # ------------------------------------------------------------------------ #

    def get_data_from_line(self, line):
        """De una linea de texto, obtiene la medida"""
        dictionary = {"Value": None, "Error (%)": None, "Unit": None}

        # Unit
        if 'Joules' in line:
            dictionary["Unit"] = 'Joules'
        elif 'seconds' in line:
            dictionary["Unit"] = 'Seconds'
        elif 'instructions' in line:
            dictionary["Unit"] = 'Instructions'
        else:
            return None

        # Value
        words = line.split()
        if 'instructions' in line:
            dictionary["Value"] = float(words[0].replace('.', ''))
        else:
            dictionary["Value"] = float(words[0].replace(',', '.'))

        # Error
        for w in words:
            if '%' in w:
                dictionary["Error (%)"] = float(
                    w.replace(',', '.').replace('%', ''))

        return dictionary
    # ------------------------------------------------------------------------ #

    def dict_to_array(self, array, events, dicts):
        """A partir de un diccionario, separa los eventos en arrays. Devuelve
        dichos arrays dentro de un array."""
        for entry in dicts:
            for i in range(0, len(events)):
                if entry["Event"] == events[i]:
                    array[i].append(int(entry["Value"]))
        return array
    # ------------------------------------------------------------------------ #

    def normaliza(self, array_1, array_2, events, vector):
        """casa"""
        array = [[] for _ in range(len(events))]
        for i in range(0, len(events)):
            for j in range(0, len(vector)):
                aux = array_1[i][j] - array_2[i][j]
                array[i].append(0 if aux < 0 else aux)
        return array

    # ------------------------------------------------------------------------ #

    def calcula_IPC_from_array(self, array, sobreescribe):
        """casa"""

        ipc = []
        instructions = array[-1]  # Depende del orden de los eventos
        cycles = array[-2]

        for i in range(0, len(instructions)):
            if cycles[i] != 0:
                ipc.append(instructions[i] / cycles[i])
            else:
                ipc.append(0)

        if sobreescribe:
            del array[-1]  # Elimina las instructions
            del array[-1]  # Elimina los cycles

        array.append(ipc)  # Ahora es el nuevo ultimo elemento
        return array
    # ------------------------------------------------------------------------ #

    def calcula_IPC_from_dicts(self, dict, sobreescribe):
        """"""
        instructions, cycles, ipc = [], [], []
        for key, value in dict.items():
            if key == "instructions":
                instructions = value
            elif key == "cycles":
                cycles = value
            else:
                continue

        # Comprobacion
        if len(instructions) == 0 or len(cycles) == 0:
            return None

        for i in range(0, len(instructions)):
            print("i=", i, " Len=", len(instructions))
            if (cycles[i] != 0):
                ipc.append(instructions[i] / cycles[i])
            else:
                ipc.append(0)

        if sobreescribe:
            del dict["instructions"]
            del dict["cycles"]
        dict["IPC"] = ipc

        return dict
    # ------------------------------------------------------------------------ #
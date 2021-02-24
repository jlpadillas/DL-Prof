#!/usr/bin/env bash


# Usage
usage () {
    cat <<HELP_USAGE
Usage: tlev.sh [[Program] | [Options]]

Program:
    Utiliza el programa toplev para realizar medidas top-dow del programa que se
    pasa como parametro [Program].

    Ejecuta el programa "mat_mul.py" pasándole el mismo parámetro que se introduzca
    al ejecutar este programa.

Options:
   -h, --help
        show this message and exit.
HELP_USAGE
}

if [[ -z $1 ]] || [[ $1 = "--help" ]] || [[ $1 = "-h" ]]; then
    usage
    exit
fi
# ------------------------------------------------------------------------ #

# Variables
PYTHON=`which python3`
SRC_DIR=src
# TODO: Fill with the "toplev.py" path or let the program find it
# TLEV=
# The first time, it finds the program and saves it in a hidden file
# for future executions.
if [ -z "$TLEV" ]; then
    FILE=.tlev.sh_variables.txt
    if [[ ! -e ${SRC_DIR}/${FILE} ]]; then
        TLEV=`find / -name "toplev.py" 2> /dev/null`
        echo $TLEV > ${SRC_DIR}/${FILE}
    else
        TLEV=$(<${SRC_DIR}/${FILE})
    fi
fi
# TLGRAPH = /home/jlpadillas01/pmu-tools/tl-barplot.py
# Basta con anhadir --graph a tlev para que se repsente el resultado en una grafica
# ------------------------------------------------------------------------ #

# Start measure
sudo sysctl -w kernel.nmi_watchdog=0 > /dev/null
sudo ${TLEV} --core C0 -l4 --no-desc --raw taskset -c 0 ${PYTHON} ${SRC_DIR}/mat_mul.py $1
# sudo ${TLEV} --core C0 -l4 --no-desc taskset -c 0 ${PYTHON} ${SRC_DIR}/mat_mul.py $1
sudo sysctl -w kernel.nmi_watchdog=1 > /dev/null
# ------------------------------------------------------------------------ #

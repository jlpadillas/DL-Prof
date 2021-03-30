#!/usr/bin/env bash


# Usage
usage () {
    cat <<HELP_USAGE
Usage: perf.sh [[Program] | [Options]]

Program:
    Utiliza el comando perf para medir las operaciones de punto flotante que
    se producen durante la ejecución del programa [Program].

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
PERF=`which perf`
EVENTS=`perf list | grep fp_ | mawk '{print}' ORS=',' | sed 's/ //g'`cycles\
,instructions
SRC_DIR="src"
# PROGRAM="mat_mul.py"
PROGRAM=$1
PARAMS=$2
# ------------------------------------------------------------------------ #

# Start singlethread measure
sudo sysctl -w kernel.nmi_watchdog=0 > /dev/null # Disable NMI
sudo sysctl -w kernel.perf_event_paranoid=0 > /dev/null # Allow perf measure

# TODO: Cambiar si estamos midiendo en python
# sudo ${PERF} stat --event ${EVENTS} --cpu=0 taskset -c 0 ${PYTHON} \
#     ${SRC_DIR}/${PROGRAM} ${PARAMS}

# TODO: O estamos midiendo el main en C
sudo ${PERF} stat --event ${EVENTS} --cpu=0 taskset -c 0 ./bin/main

sudo sysctl -w kernel.perf_event_paranoid=4 > /dev/null # Back to normal
sudo sysctl -w kernel.nmi_watchdog=1 > /dev/null # Enable NMI
# ------------------------------------------------------------------------ #

# # Start multithread measure
# sudo sysctl -w kernel.nmi_watchdog=0 > /dev/null # Disable NMI
# sudo sysctl -w kernel.perf_event_paranoid=0 > /dev/null # Allow perf measure
# sudo ${PERF} stat --event ${EVENTS} --cpu=0 taskset -c 0 ${PYTHON} \
#     ${SRC_DIR}/${PROGRAM} $1
# sudo sysctl -w kernel.perf_event_paranoid=4 > /dev/null # Back to normal
# sudo sysctl -w kernel.nmi_watchdog=1 > /dev/null # Enable NMI
# # ------------------------------------------------------------------------ #
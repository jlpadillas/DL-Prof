#!/usr/bin/env bash

# ------------------------------------------------------------------------ #
# __author__ = "Juan Luis Padilla Salomé"
# __copyright__ = "Copyright 2021"
# __credits__ = ["University of Cantabria"]
# __license__ = "GPL"
# __version__ = "1.0.0"
# __maintainer__ = "Juan Luis Padilla Salomé"
# __email__ = "juan-luis.padilla@alumnos.unican.es"
# __status__ = "Production"
# ------------------------------------------------------------------------ #

# ------------------------------------------------------------------------ #
# Error handling
set -e

err_report() {
    echo "Error on line $1"
}

trap 'err_report $LINENO' ERR

echoerr() { printf "%s\n" "$*" >&2; }

# ------------------------------------------------------------------------ #
# Usage
usage () {
    cat <<HELP_USAGE
Usage: perf.sh [[Program] [Parameters] | [Options]]

Program:
    It uses the perf command to measure floating point operations that occur
    during the execution of the program [Program].

    The program accepts binary and python files.

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
PERF=$(which perf)
if [[ -z $PERF ]]; then
    echo "[ERROR] The program needs to have perf installed." >&2
    exit 1
else
    EVENTS=$(perf list | grep fp_ | mawk '{print}' ORS=',' | sed 's/ //g')
    EVENTS=instructions,cycles,${EVENTS%,}
fi

# Saves the name of the program to execute and its parameters
PROGRAM=$1
PARAMS=""
if [ "$#" -gt 1 ]; then
    # PARAMS="${@:2}"
    PARAMS=("${@:2}")
fi

# Check if the program has an extension (.py, .c, .something)
EXEC=""
FILE_NAME=$PROGRAM
FILE_EXTN=""
if [[ $PROGRAM == *"."* ]]; then # It has an extension
    FILE_EXTN=$(echo "$PROGRAM" | rev | cut -d'.' -f1 | rev)
    FILE_NAME=${FILE_NAME%.$FILE_EXTN}

    # Check if it is a python program and modify the exec
    if [[ $FILE_EXTN == "py" ]]; then
        EXEC=$(which python3)
    else
        echoerr "[ERROR] Extension '$FILE_EXTN' not supported."
        exit 1
    fi
fi

# ------------------------------------------------------------------------ #
# Start measure
sudo sysctl -w kernel.nmi_watchdog=0 > /dev/null # Disable NMI
sudo sysctl -w kernel.perf_event_paranoid=0 > /dev/null # Allow perf measure

if [[ $FILE_EXTN == "" ]]; then
    sudo "${PERF}" stat --event "${EVENTS}" --cpu=0 taskset -c 0 \
        "${PROGRAM}" "${PARAMS[@]}"
else
    sudo "${PERF}" stat --event "${EVENTS}" --cpu=0 taskset -c 0 "${EXEC}" \
        "${PROGRAM}" "${PARAMS[@]}"
fi

sudo sysctl -w kernel.perf_event_paranoid=4 > /dev/null # Back to normal
sudo sysctl -w kernel.nmi_watchdog=1 > /dev/null # Enable NMI
# ------------------------------------------------------------------------ #

# TODO: Tratar el resultado obtenido en PERF para que sea más fácil de leer?
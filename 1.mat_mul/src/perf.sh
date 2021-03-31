#!/usr/bin/env bash

# ------------------------------------------------------------------------ #




# ------------------------------------------------------------------------ #
# Error handling
set -e

err_report() {
    echo "Error on line $1"
}

trap 'err_report $LINENO' ERR

echoerr() { printf "%s\n" "$*" >&2; }
# echoerr hello world

# trap 'echoerr $LINENO' ERR


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

PERF=`which perf`
if [[ -z $PERF ]]; then
    echo "[ERROR] The program needs to have perf installed." >&2
    exit -1
else
    EVENTS=`perf list | grep fp_ | mawk '{print}' ORS=',' | sed 's/ //g'`
    EVENTS=instructions,cycles,${EVENTS%,}
fi

# Saves the name of the program to execute and its parameters
PROGRAM=$1
PARAMS=""
if [ "$#" -gt 1 ]; then
    PARAMS="${@:2}"
fi

# Check if the program has an extension (.py, .c, .something)
EXEC=""
FILE_NAME=$PROGRAM
FILE_EXTN=""
if [[ $PROGRAM == *"."* ]]; then # It has an extension
    FILE_NAME=`echo "$PROGRAM" | cut -d'.' -f1`
    FILE_EXTN=`echo "$PROGRAM" | cut -d'.' -f2`

    # Check if it is a python program and modify the exec
    if [[ $FILE_EXTN == "py" ]]; then
        EXEC=`which python3`
    else
        echoerr "[ERROR] Extension '$FILE_EXTN' not supported."
        exit -1
    fi
fi

SRC_DIR="src"

exit

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
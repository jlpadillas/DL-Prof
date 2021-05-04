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
# Functions
# ------------------------------------------------------------------------ #
set_environment () {
# Fija la frecuencia del CPU a una pasada por parametro y desactiva el
# turbo-boost mediante el uso de los registros msr. Si no se pasa una
# frecuencia, se fija por defecto a 2.2GHz. Formato de la frecuencia
# permitida: 800MHz, 1.9GHz, etc.
# Note. Necesario tener instalado el paquete 'msr-tools'
  # Se fija la frecuencia de la CPU
  local FREQ=2.2GHz
  local MSR="0x1a0"
  local CODE="0x4000850089"
  # Carga libreria para hacer cambios en los registros msr
  sudo modprobe msr
  # Se deshabilita el turboboost de Intel
  sudo wrmsr --all $MSR $CODE
  # Establece el governor del CPU
  sudo cpupower frequency-set --governor userspace
  # Establece la frecuencia del CPU
  sudo cpupower frequency-set --freq $FREQ
}

# ------------------------------------------------------------------------ #
# Error handling
# ------------------------------------------------------------------------ #
set -e

err_report() {
    echo "[PERF] Error on line $1"
}

trap 'err_report $LINENO' ERR

echoerr() { printf "%s\n" "$*" >&2; }

# ------------------------------------------------------------------------ #
# Usage
# ------------------------------------------------------------------------ #
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
   -p, --papi
        executes the program and dont measure it with perf
   -t, --taskset
        executes the program only on the list of CPUs provided. Receives a
        numerical list of processors. Numbers are separated by commas and
        may include ranges. e.g: 0,5,8-11
HELP_USAGE
}

if [[ -z $1 ]] || [[ $1 = "--help" ]] || [[ $1 = "-h" ]]; then
    usage
    exit
fi

# ------------------------------------------------------------------------ #
# Read arguments
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -p|--papi)
        PAPI=YES
        shift # past argument
        ;;
        -t|--taskset)
        CPU="$2"
        shift # past argument
        shift # past value
        ;;
        # -s|--searchpath)
        # SEARCHPATH="$2"
        # shift # past argument
        # shift # past value
        # ;;
        # -l|--lib)
        # LIBPATH="$2"
        # shift # past argument
        # shift # past value
        # ;;
        *)    # unknown option
        POSITIONAL+=("$1") # save it in an array for later
        shift # past argument
        ;;
    esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

# ------------------------------------------------------------------------ #
# Variables
# ------------------------------------------------------------------------ #
PERF=$(which perf)
if [[ -z $PERF ]]; then
    echo "[PERF] Error, the program needs to have perf installed." >&2
    exit 1
else
    EVENTS=$($PERF list | grep fp_ | mawk '{print}' ORS=',' | sed 's/ //g')
    if [[ -z ${EVENTS+x} ]]; then # There is no fp events
        EVENTS=cycles,instructions
    else
        EVENTS=cycles,instructions,${EVENTS%,}
    fi
fi

# Format of the perf output
# FORMAT=-x:
FORMAT=""

# Saves the name of the program to execute and its parameters
PROGRAM=$1
PARAMS=""
if [ "$#" -gt 1 ]; then
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
    # TODO: modify lines for permit execute *.out files
    # else
    #     # Check if it's: ./[anything]
    #     if ! [[ $FILE_EXTN == /* ]]; then
    #         echoerr "[ERROR] Extension '$FILE_EXTN' not supported."
    #         exit 1
    #     fi
    fi
fi

# The command that will be executed
COMMAND="" # Not a sudo command

if [[ -z ${PAPI+x} ]]; then # Executing WITHOUT PAPI (using PERF)
    COMMAND="${COMMAND} ${PERF} stat ${FORMAT} --event ${EVENTS}"
fi

# Check the taskset param
if [[ -n ${CPU} ]]; then
    if [[ -z ${PAPI+x} ]]; then # PERF measures the same CPUs
        COMMAND="${COMMAND} --cpu=${CPU}"
    fi
    COMMAND="${COMMAND} taskset --cpu-list ${CPU}"
fi

# Check if it is a binary or need a program to be executed (python)
if [[ -n ${EXEC} ]]; then
    COMMAND="${COMMAND} ${EXEC}"
fi

# Pass the program and its params
COMMAND="${COMMAND} ${PROGRAM} ${PARAMS[*]}"

# ------------------------------------------------------------------------ #
# Start measure
# ------------------------------------------------------------------------ #
# sudo sysctl -w kernel.nmi_watchdog=0 > /dev/null # Disable NMI
# sudo sysctl -w kernel.perf_event_paranoid=0 > /dev/null # Allow perf measure

eval "${COMMAND}" # Run the command generated

# sudo sysctl -w kernel.perf_event_paranoid=4 > /dev/null # Back to normal
# sudo sysctl -w kernel.nmi_watchdog=1 > /dev/null # Enable NMI
# ------------------------------------------------------------------------ #

exit 0
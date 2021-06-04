# --------------------------------------------------------------------------- #

# @author: 
.PHONY = all setup
.DEFAULT_GOAL = compile
# --------------------------------------------------------------------------- #

# Directory where binaries are saved
BIN_DIR = bin
# Directory where configuration files are saved
CFG_DIR = conf
# Directory where libraries are saved
LIB_DIR = lib
# Directory where result files are saved
OUT_DIR = out
# Directory where scripts are saved
SRC_DIR = src
# Compiler to use
CC = python3
# Events to measure with perf
EVENTS = $(shell perf list | grep fp_ | mawk '{print}' ORS=',' | sed 's/ //g')cycles,instructions
# --------------------------------------------------------------------------- #

# Absolute path to the parent of this Makefile (/[path_before_TFG]/TFG/test/C)
MAKEFILE_PATH := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
# Absolute path to my_papi library (/[path_before_TFG]/TFG/my_papi)
MP_PATH = $(realpath ${MAKEFILE_PATH}/../../../my_papi)
# --------------------------------------------------------------------------- #

all: setup compile

setup:
	mkdir -p ${OUT_DIR}

compile:
# Compile my_papi library
	make -C ${MP_PATH} compile
# --------------------------------------------------------------------------- #

run:
# Executing the program with my_papi library for Python
	taskset -c 2-31 ${CC} ${SRC_DIR}/main_papi.py SEQ 1024
	taskset -c 2-31 ${CC} ${SRC_DIR}/main_papi.py RAND 1024
	taskset -c 2-31 ${CC} ${SRC_DIR}/main_papi.py EMPTY 1024
	taskset -c 2 ${CC} ${SRC_DIR}/main_papi.py SEQ 1024
# taskset -c 2 ${CC} ${SRC_DIR}/main_papi.py SEQ 4096

run_with_perf:
# Executing the program and measures with perf
	taskset -c 2-31 perf stat -e ${EVENTS} ${CC} ${SRC_DIR}/main.py SEQ 4096
# taskset -c 2 perf stat -e ${EVENTS} ${CC} ${SRC_DIR}/main.py SEQ 4096
# --------------------------------------------------------------------------- #

# ! Permissions are needed to execute the perf/PAPI commands w/o sudo
permissions_disabled:
# Not allow perf measure and enable NMI
	sudo sysctl -w kernel.perf_event_paranoid=4 > /dev/null
	sudo sysctl -w kernel.nmi_watchdog=1 > /dev/null

permissions_enabled:
# Disable NMI and allow perf measure
	sudo sysctl -w kernel.nmi_watchdog=0 > /dev/null
	sudo sysctl -w kernel.perf_event_paranoid=0 > /dev/null
# --------------------------------------------------------------------------- #

send_results:
# ? Send the results from the node to the host machine
	scp out/* jlpadillas01@193.144.198.240:/home/jlpadillas01/Descargas/

get_results:
# ? Get the results from the node
	scp juan@calderon.atc.unican.es:~/TFG/tests/mat_mul/Python/out/*csv ${MAKEFILE_PATH}/out/
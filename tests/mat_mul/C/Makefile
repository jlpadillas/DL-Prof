# --------------------------------------------------------------------------- #

# @author: 
.PHONY = all clean setup
.DEFAULT_GOAL = compile
# --------------------------------------------------------------------------- #

# Directory where binaries are saved
BIN_DIR = bin
# Directory where libraries are saved
LIB_DIR = lib
# Directory where result files are saved
OUT_DIR = out
# Directory where scripts are saved
SRC_DIR = src
# Flags used to compile c files
CFLAGS = -Wall -Werror
# Compiler to use
CC = gcc
# Events to measure with perf
EVENTS = $(shell perf list | grep fp_ | mawk '{print}' ORS=',' | sed 's/ //g')cycles,instructions
# --------------------------------------------------------------------------- #

# Absolute path to the parent of this Makefile (/[path_before_TFG]/TFG/test/C)
MAKEFILE_PATH := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
# Absolute path to my_papi library (/[path_before_TFG]/TFG/my_papi)
MP_PATH = $(realpath ${MAKEFILE_PATH}/../../../my_papi)

MP_LIB_DIR = ${MP_PATH}/${LIB_DIR}
MP_SRC_DIR = ${MP_PATH}/${SRC_DIR}
# --------------------------------------------------------------------------- #

all: clean setup compile

clean:
	rm -rf ${BIN_DIR}/*

setup:
	mkdir -p ${BIN_DIR} ${OUT_DIR}

compile:
# my_papi library
	make -C ${MP_PATH} compile
# matrix and main files
	${CC} ${CFLAGS} -c ${SRC_DIR}/matrix.c -o ${BIN_DIR}/matrix.o
	${CC} ${CFLAGS} ${SRC_DIR}/main.c -o ${BIN_DIR}/main_perf \
		${BIN_DIR}/matrix.o -pthread
	${CC} ${CFLAGS} ${SRC_DIR}/main.c -o ${BIN_DIR}/main_papi -DMY_PAPI \
		-Wl,-rpath=${MP_LIB_DIR} ${BIN_DIR}/matrix.o -I${MP_SRC_DIR} \
		-L${MP_LIB_DIR} -lmy_papi -pthread
# --------------------------------------------------------------------------- #

run:
# Executing the program with my_papi library
	./${BIN_DIR}/main_papi SEQ 512 NORMAL
	./${BIN_DIR}/main_papi SEQ 512 TRANSPOSE
	./${BIN_DIR}/main_papi SEQ 512 MULTITHREAD
	taskset -c 0 ./${BIN_DIR}/main_papi SEQ 512 MULTITHREAD
# --------------------------------------------------------------------------- #

run_with_perf:
# Executing the program and measures with perf
	perf stat -e ${EVENTS} ./${BIN_DIR}/main_perf SEQ 512 NORMAL
	perf stat -e ${EVENTS} ./${BIN_DIR}/main_perf SEQ 512 TRANSPOSE
	perf stat -e ${EVENTS} ./${BIN_DIR}/main_perf SEQ 512 MULTITHREAD
	taskset -c 0 perf stat -e ${EVENTS} ./${BIN_DIR}/main_perf SEQ 512 MULTITHREAD
# --------------------------------------------------------------------------- #

test:
# Compile my_papi library
	make -C ${MP_PATH} compile
# Compile and execute test file
	${CC} ${CFLAGS} ${SRC_DIR}/test.c -o ${BIN_DIR}/test -DMY_PAPI \
		-Wl,-rpath=${MP_LIB_DIR} ${BIN_DIR}/matrix.o -L${MP_LIB_DIR} -lmy_papi \
		-I${MP_SRC_DIR} -pthread
	./${BIN_DIR}/test
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
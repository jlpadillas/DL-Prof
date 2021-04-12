# --------------------------------------------------------------------------- #
.PHONY = clean setup
.DEFAULT_GOAL = clean

# --------------------------------------------------------------------------- #
# Directory where scripts are saved
SRC_DIR = src
# Directory where binaries are saved
BIN_DIR = bin
# Directory where result files are saved
OUT_DIR = out
# Directory where result files are saved
LIB_DIR = lib
# Flags used to compile c files
CFLAGS = -Wall -Werror
CC = gcc
# --------------------------------------------------------------------------- #
clean:
	rm -rf bin/* lib/*

setup:
	mkdir -p ${SRC_DIR} ${BIN_DIR} ${OUT_DIR} ${LIB_DIR}

# --------------------------------------------------------------------------- #
# C FILES
matrix:
	gcc ${CFLAGS} ${SRC_DIR}/matrix.c -o ${BIN_DIR}/matrix -c -pthread

compile: matrix
	gcc ${CFLAGS} ${SRC_DIR}/main.c -o ${BIN_DIR}/main ${BIN_DIR}/matrix -pthread

c_main: compile
	./${BIN_DIR}/main RAND 500 NORMAL

c_main_multithread: compile
	./${BIN_DIR}/main_multithread

c_perf: compile
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main RAND 500 NORMAL

c_perf_multithread: compile
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main_multithread

c_perf_taskset: compile
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main --taskset

c_perf_multithread_takset: compile
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main_multithread --taskset

# --------------------------------------------------------------------------- #
# PYTHON FILES
# py_main:
# 	python3 ${SRC_DIR}/main.py zeros

# py_main_multithread:
# 	@@echo "Hola"

py_perf:
	bash ${SRC_DIR}/perf.sh ${SRC_DIR}/main.py zeros

py_perf_multithread:
	@@echo Hola

py_perf_taskset:
	bash ${SRC_DIR}/perf.sh ${SRC_DIR}/main.py zeros --taskset

py_perf_multithread_taskset:
	@@echo hola
# --------------------------------------------------------------------------- #

execution:
	bash execution.sh






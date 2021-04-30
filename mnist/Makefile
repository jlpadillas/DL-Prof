# --------------------------------------------------------------------------- #
# @author: 
.PHONY = clean
.DEFAULT_GOAL = all

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
CC = gcc

INCLUDE = -I./${SRC_DIR}

PERF_PATH=../1.mat_mul/${SRC_DIR}/perf.sh
# --------------------------------------------------------------------------- #
all: clean setup
clean:
	rm -rf ${BIN_DIR}/* ${LIB_DIR}/*

setup:
	mkdir -p ${BIN_DIR} ${LIB_DIR} ${OUT_DIR} ${SRC_DIR}
# Copies the lib to this location
	cp ../mat_mul/${LIB_DIR}/* ${LIB_DIR}/

perf:
	bash ${PERF_PATH} ${SRC_DIR}/mnist_1epoch_1thread.py
	# bash ${SRC_DIR}/perf.sh mnist_1epoch_1thread.py

# perf -e XXXX -C <n> taskset -c <n>x mnist_1epoch_1thread.py
perf_taskset:
	bash ${PERF_PATH} ${SRC_DIR}/mnist_1epoch_1thread.py --taskset

papi:
	python3 ${SRC_DIR}/mnist_1epoch_1thread_papi.py

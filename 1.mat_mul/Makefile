# --------------------------------------------------------------------------- #
# .PHONY defines parts of the makefile that are not dependant on any specific
# file
# This is most often used to store functions
.PHONY = perf tlev clean

# Defines the default target that `make` will to try to make, or in the case of
# a phony target, execute the specified commands. This target is executed
# whenever we just type `make`
.DEFAULT_GOAL = clean

# --------------------------------------------------------------------------- #
# Directory where scripts are saved
SRC_DIR = src
# Directory where binaries are saved
BIN_DIR = bin
# Directory where result files are saved
OUT_DIR = out
# Flags used to compile c files
CFLAGS = -Wall -Werror
# --------------------------------------------------------------------------- #
clean:
	rm -rf bin/*

setup:
	mkdir -p ${SRC_DIR} ${BIN_DIR} ${OUT_DIR}

# --------------------------------------------------------------------------- #
# C FILES
compile:
	gcc ${CFLAGS} -c ${SRC_DIR}/matrix.c -o ${BIN_DIR}/matrix -pthread
	gcc ${CFLAGS} ${SRC_DIR}/main.c -o ${BIN_DIR}/main ${BIN_DIR}/matrix -pthread
	gcc ${CFLAGS} ${SRC_DIR}/main_multithread.c -o ${BIN_DIR}/main_multithread \
		${BIN_DIR}/matrix -pthread

c_main: compile
	./${BIN_DIR}/main

c_main_multithread: compile
	./${BIN_DIR}/main_multithread

c_perf: compile
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main

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

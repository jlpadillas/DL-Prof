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

# --------------------------------------------------------------------------- #
clean:
	rm -rf bin/*

setup:
	mkdir -p ${SRC_DIR} ${BIN_DIR} ${OUT_DIR}

perf:
	bash ${SRC_DIR}/perf.sh ${SRC_DIR}/main.py zeros

tlev:
	bash ${SRC_DIR}/tlev.sh main.py zeros

matrix:
	gcc -Wall -Werror -c ${SRC_DIR}/matrix.c -pthread -o ${BIN_DIR}/matrix

main_c: matrix
	gcc -Wall ${SRC_DIR}/main.c -pthread -o ${BIN_DIR}/main ${BIN_DIR}/matrix
	./${BIN_DIR}/main

main_multithread_c: matrix
	gcc -Wall ${SRC_DIR}/main_multithread.c -pthread \
		-o ${BIN_DIR}/main_multi ${BIN_DIR}/matrix
	./${BIN_DIR}/main_multi

perf_c:
	bash ${SRC_DIR}/perf.sh main
# --------------------------------------------------------------------------- #
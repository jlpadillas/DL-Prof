# --------------------------------------------------------------------------- #
# .PHONY defines parts of the makefile that are not dependant on any specific file
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

perf:
	bash ${SRC_DIR}/perf.sh main.py zeros

tlev:
	bash ${SRC_DIR}/tlev.sh main.py zeros

main_c:
	gcc -Wall -c ${SRC_DIR}/matrix.c -o ${BIN_DIR}/matrix
	gcc -Wall ${SRC_DIR}/main.c -o ${BIN_DIR}/main ${BIN_DIR}/matrix
	./${BIN_DIR}/main

python:
	python3 ${SRC_DIR}/papi_main.py zeros
# --------------------------------------------------------------------------- #
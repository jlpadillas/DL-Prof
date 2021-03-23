.PHONY = clean
.DEFAULT_GOAL = all

# --------------------------------------------------------------------------- #
CC = gcc
CFLAGS = -Wall -Werror

# Directory where scripts are saved
SRC_DIR = src
# Directory where binaries are saved
BIN_DIR = bin
# Directory where result files are saved
OUT_DIR = out
# Directory where the library is saved
LIB_DIR = lib

INCLUDE = -I./${SRC_DIR}

# --------------------------------------------------------------------------- #
all: perf

perf:
	# perf -e XXXX -C <n> taskset -c <n>x mnist_1epoch_1thread.py
	bash ${SRC_DIR}/perf.sh 1


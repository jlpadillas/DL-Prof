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
	mkdir -p src/ bin/ out/ lib/

# perf -e XXXX -C <n> taskset -c <n>x mnist_1epoch_1thread.py
perf_taskset:
	bash ${SRC_DIR}/perf_taskset.sh mnist_1epoch_1thread.py

perf:
	bash ${SRC_DIR}/perf.sh mnist_1epoch_1thread.py

papi:
	python3 ${SRC_DIR}/mnist_1epoch_1thread_papi.py

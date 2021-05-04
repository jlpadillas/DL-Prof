# --------------------------------------------------------------------------- #
# @author: 
.PHONY = all clean setup
.DEFAULT_GOAL = clean

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
# --------------------------------------------------------------------------- #
all: clean setup

clean:
	rm -rf ${BIN_DIR}/* ${LIB_DIR}/*

setup:
	mkdir -p ${BIN_DIR} ${LIB_DIR} ${OUT_DIR} ${SRC_DIR}

# --------------------------------------------------------------------------- #
# C FILES
test_compile: my_papi
# Compiling
	${CC} ${CFLAGS} -c ${SRC_DIR}/matrix.c -o ${BIN_DIR}/matrix.o
	${CC} ${CFLAGS} ${SRC_DIR}/main.c -o ${BIN_DIR}/main_perf \
		${BIN_DIR}/matrix.o -pthread
	${CC} ${CFLAGS} ${SRC_DIR}/main.c -o ${BIN_DIR}/main_papi -DMY_PAPI \
		-Wl,-rpath=${LIB_DIR} ${BIN_DIR}/matrix.o -L${LIB_DIR} -lmy_papi \
		-pthread

test_run: test_compile
# Executing
	./${BIN_DIR}/main_papi SEQ 512 TRANSPOSE
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main_perf SEQ 512 TRANSPOSE
	./${BIN_DIR}/main_papi SEQ 512 MULTITHREAD
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main_perf SEQ 512 MULTITHREAD

my_papi:
# my_papi library
	${CC} ${CFLAGS} -fPIC -c ${SRC_DIR}/my_papi.c -o ${BIN_DIR}/my_papi.o
	${CC} -shared -o ${LIB_DIR}/libmy_papi.so ${BIN_DIR}/my_papi.o \
		-L/usr/local/lib -lpapi

# --------------------------------------------------------------------------- #
# ! Permissions
permissions_disabled:
# Back to normal and enable NMI
	sudo sysctl -w kernel.perf_event_paranoid=4
	sudo sysctl -w kernel.nmi_watchdog=1

permissions_enabled:
# Disable NMI and allow perf measure
	sudo sysctl -w kernel.nmi_watchdog=0
	sudo sysctl -w kernel.perf_event_paranoid=0

# --------------------------------------------------------------------------- #
execution:
	bash execution.sh

borrar:
	${CC} ${CFLAGS} -c ${SRC_DIR}/matrix.c -o ${BIN_DIR}/matrix.o
	${CC} ${CFLAGS} ${SRC_DIR}/test.c -o ${BIN_DIR}/test -DMY_PAPI \
		-Wl,-rpath=${LIB_DIR} ${BIN_DIR}/matrix.o -L${LIB_DIR} -lmy_papi \
		-pthread
	./${BIN_DIR}/test
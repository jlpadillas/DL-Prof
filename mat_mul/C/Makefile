# --------------------------------------------------------------------------- #
# @author: 
.PHONY = all clean setup
.DEFAULT_GOAL = clean

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
# Flags used to compile c files
CFLAGS = -Wall -Werror
CC = gcc
# --------------------------------------------------------------------------- #
all: clean setup

clean:
	rm -rf ${BIN_DIR}/* ${LIB_DIR}/*

setup:
	mkdir -p ${BIN_DIR} ${CFG_DIR} ${LIB_DIR} ${OUT_DIR} ${SRC_DIR}

# --------------------------------------------------------------------------- #
compile: my_papi
# Compiling
	${CC} ${CFLAGS} -c ${SRC_DIR}/matrix.c -o ${BIN_DIR}/matrix.o
	${CC} ${CFLAGS} ${SRC_DIR}/main.c -o ${BIN_DIR}/main_perf \
		${BIN_DIR}/matrix.o -pthread
	${CC} ${CFLAGS} ${SRC_DIR}/main.c -o ${BIN_DIR}/main_papi -DMY_PAPI \
		-Wl,-rpath=${LIB_DIR} ${BIN_DIR}/matrix.o -L${LIB_DIR} -lmy_papi \
		-pthread

# --------------------------------------------------------------------------- #
# Executing
run_multithread:
	./${BIN_DIR}/main_papi SEQ 512 MULTITHREAD
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main_perf SEQ 512 MULTITHREAD

run:
	./${BIN_DIR}/main_papi SEQ 512 NORMAL
	./${BIN_DIR}/main_papi SEQ 512 TRANSPOSE
	taskset -c 0 ./${BIN_DIR}/main_papi SEQ 512 MULTITHREAD
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main_perf SEQ 512 NORMAL
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main_perf SEQ 512 TRANSPOSE

# --------------------------------------------------------------------------- #
my_papi:
# my_papi library
	${CC} ${CFLAGS} -fPIC -c ${SRC_DIR}/my_papi.c -o ${BIN_DIR}/my_papi.o
	${CC} -shared -o ${LIB_DIR}/libmy_papi.so ${BIN_DIR}/my_papi.o \
		-L/usr/local/lib -lpapi
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# ! Permissions
permissions_disabled:
# Back to normal and enable NMI
	sudo sysctl -w kernel.perf_event_paranoid=4 > /dev/null
	sudo sysctl -w kernel.nmi_watchdog=1 > /dev/null

permissions_enabled:
# Disable NMI and allow perf measure
	sudo sysctl -w kernel.nmi_watchdog=0 > /dev/null
	sudo sysctl -w kernel.perf_event_paranoid=0 > /dev/null

# --------------------------------------------------------------------------- #
execution:
	bash execution.sh

test: my_papi
	${CC} ${CFLAGS} -c ${SRC_DIR}/matrix.c -o ${BIN_DIR}/matrix.o
	${CC} ${CFLAGS} ${SRC_DIR}/test.c -o ${BIN_DIR}/test -DMY_PAPI \
		-Wl,-rpath=${LIB_DIR} ${BIN_DIR}/matrix.o -L${LIB_DIR} -lmy_papi \
		-pthread
	./${BIN_DIR}/test

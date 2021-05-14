# --------------------------------------------------------------------------- #
# @author: 
.PHONY = all clean setup
.DEFAULT_GOAL = compile

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
all: clean setup compile

clean:
	rm -rf ${BIN_DIR}/* ${LIB_DIR}/*

setup:
	mkdir -p ${BIN_DIR} ${CFG_DIR} ${LIB_DIR} ${OUT_DIR} ${SRC_DIR}

# --------------------------------------------------------------------------- #
compile:
# Compile my_papi library
	${CC} ${CFLAGS} -fPIC -c ${SRC_DIR}/my_papi.c -o ${BIN_DIR}/my_papi.o
	${CC} -shared -o ${LIB_DIR}/libmy_papi.so ${BIN_DIR}/my_papi.o \
		-L/usr/local/lib -lpapi

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

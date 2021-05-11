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
CC = python3
# --------------------------------------------------------------------------- #
all: clean setup compile

clean:
	rm -rf ${BIN_DIR}/* ${LIB_DIR}/*

setup:
	mkdir -p ${BIN_DIR} ${CFG_DIR} ${LIB_DIR} ${OUT_DIR} ${SRC_DIR}

# --------------------------------------------------------------------------- #
# Getting the my_papi lib
PYTHON_PATH = ../../mat_mul/Python
compile:
	make -C ${PYTHON_PATH} compile
	cp ${PYTHON_PATH}/${LIB_DIR}/* ${LIB_DIR}/
	cp ${PYTHON_PATH}/${SRC_DIR}/system_setup.py ${SRC_DIR}/
	cp ${PYTHON_PATH}/${SRC_DIR}/my_papi.py ${SRC_DIR}/

# --------------------------------------------------------------------------- #
PERF_PATH=../1.mat_mul/${SRC_DIR}/perf.sh
# --------------------------------------------------------------------------- #
papi:
	python3 ${SRC_DIR}/main.py

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

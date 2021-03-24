.PHONY = clean
.DEFAULT_GOAL = all

# --------------------------------------------------------------------------- #
# Directory where scripts are saved
SRC_DIR = src
# Directory where binaries are saved
BIN_DIR = bin
# Directory where result files are saved
OUT_DIR = out
# Directory where the library is saved
LIB_DIR = lib

# --------------------------------------------------------------------------- #
CC = gcc
CFLAGS = -Wall -Werror
INCLUDE = -I./${SRC_DIR}

# --------------------------------------------------------------------------- #
all: my_papi main execute

my_papi:
	${CC} ${CFLAGS} -fPIC ${INCLUDE} -c ${SRC_DIR}/my_papi.c -o ${BIN_DIR}/my_papi.o
	${CC} -shared -o ${LIB_DIR}/libmy_papi.so ${BIN_DIR}/my_papi.o -L/usr/local/lib -lpapi

main:
	${CC} ${CFLAGS} ${INCLUDE} -c ${SRC_DIR}/papi_main.c -o ${BIN_DIR}/papi_main.o
	${CC} -o ${BIN_DIR}/papi_prog ../1.mat_mul/bin/matrix ${BIN_DIR}/papi_main.o -L./${LIB_DIR} -lmy_papi

execute:
	# Importante! Si no encuentra la libreria, ejecutar el sig. comando:
	# export LD_LIBRARY_PATH=./lib:/usr/local/lib
	sudo sysctl -w kernel.nmi_watchdog=0 > /dev/null
	sudo sysctl -w kernel.perf_event_paranoid=1 > /dev/null
	./${BIN_DIR}/papi_prog
	sudo sysctl -w kernel.perf_event_paranoid=4 > /dev/null
	sudo sysctl -w kernel.nmi_watchdog=1 > /dev/null

clean:
	rm -f ${BIN_DIR}/*

echo:
	@echo $$LD_LIBRARY_PATH

# --------------------------------------------------------------------------- #
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
CC = python3
# --------------------------------------------------------------------------- #
all: clean setup

clean:
	rm -rf ${BIN_DIR}/* ${LIB_DIR}/*

setup:
	mkdir -p ${BIN_DIR} ${CFG_DIR} ${LIB_DIR} ${OUT_DIR} ${SRC_DIR}

# --------------------------------------------------------------------------- #
# Getting the my_papi lib
my_papi:
	cp ../C/${LIB_DIR}/* ${LIB_DIR}/

# --------------------------------------------------------------------------- #
# Pytohn FILES
main_papi: my_papi
# PC
	${CC} ${SRC_DIR}/main_papi.py seq
	perf stat -e cycles,instructions,fp_assist.any,fp_assist.simd_input,fp_assist.simd_output,fp_assist.x87_input,fp_assist.x87_output,fp_comp_ops_exe.sse_packed_double,fp_comp_ops_exe.sse_packed_single,fp_comp_ops_exe.sse_scalar_double,fp_comp_ops_exe.sse_scalar_single,fp_comp_ops_exe.x87,simd_fp_256.packed_double,simd_fp_256.packed_single,arith.fpu_div,arith.fpu_div_active ${CC} ${SRC_DIR}/main.py seq

main_papi_node: my_papi
# NODE
	${CC} ${SRC_DIR}/main_papi.py seq
	perf stat -e cycles,instructions,fp_arith_inst_retired.128b_packed_double,fp_arith_inst_retired.128b_packed_single,fp_arith_inst_retired.256b_packed_double,fp_arith_inst_retired.256b_packed_single,fp_arith_inst_retired.512b_packed_double,fp_arith_inst_retired.512b_packed_single,fp_arith_inst_retired.scalar_double,fp_arith_inst_retired.scalar_single,fp_assist.any ${CC} ${SRC_DIR}/main.py seq

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
	./${BIN_DIR}/main_papi SEQ 512 MULTITHREAD
	bash ${SRC_DIR}/perf.sh ${BIN_DIR}/main_perf SEQ 512 MULTITHREAD

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

execution:
	bash execution.sh


borrar:
	${CC} ${CFLAGS} -c ${SRC_DIR}/matrix.c -o ${BIN_DIR}/matrix.o
	${CC} ${CFLAGS} ${SRC_DIR}/test.c -o ${BIN_DIR}/test -DMY_PAPI \
		-Wl,-rpath=${LIB_DIR} ${BIN_DIR}/matrix.o -L${LIB_DIR} -lmy_papi \
		-pthread
	./${BIN_DIR}/test
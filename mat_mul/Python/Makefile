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
compile:
	make -C ../C/ my_papi
	cp ../C/${LIB_DIR}/* ${LIB_DIR}/

# --------------------------------------------------------------------------- #
# PYTHON FILES
main_papi: compile
# PC
	${CC} ${SRC_DIR}/main_papi.py seq
	perf stat -e cycles,instructions,fp_assist.any,fp_assist.simd_input,fp_assist.simd_output,fp_assist.x87_input,\
	fp_assist.x87_output,fp_comp_ops_exe.sse_packed_double,fp_comp_ops_exe.sse_packed_single,fp_comp_ops_exe.sse_scalar_double,\
	fp_comp_ops_exe.sse_scalar_single,fp_comp_ops_exe.x87,simd_fp_256.packed_double,simd_fp_256.packed_single,arith.fpu_div,arith.fpu_div_active \
	${CC} ${SRC_DIR}/main.py seq

main_papi_node: compile
# NODE
	${CC} ${SRC_DIR}/main_papi.py seq
	perf stat -e cycles,instructions,fp_arith_inst_retired.128b_packed_double,fp_arith_inst_retired.128b_packed_single,fp_arith_inst_retired.256b_packed_double,\
	fp_arith_inst_retired.256b_packed_single,fp_arith_inst_retired.512b_packed_double,fp_arith_inst_retired.512b_packed_single,fp_arith_inst_retired.scalar_double,\
	fp_arith_inst_retired.scalar_single,fp_assist.any ${CC} ${SRC_DIR}/main.py seq

main_papi_node_taskset: compile
# NODE
	taskset -c 0 ${CC} ${SRC_DIR}/main_papi.py seq
	taskset -c 0 perf stat -e cycles,instructions,fp_arith_inst_retired.128b_packed_double,fp_arith_inst_retired.128b_packed_single,\
	fp_arith_inst_retired.256b_packed_double,fp_arith_inst_retired.256b_packed_single,fp_arith_inst_retired.512b_packed_double,\
	fp_arith_inst_retired.512b_packed_single,fp_arith_inst_retired.scalar_double,fp_arith_inst_retired.scalar_single,fp_assist.any \
	${CC} ${SRC_DIR}/main.py seq

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
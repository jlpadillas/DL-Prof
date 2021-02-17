# --------------------------------------------------------------------------- #
# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help setup clean papi_main

# Defines the default target that `make` will to try to make, or in the case of
# a phony target, execute the specified commands. This target is executed
# whenever we just type `make`
.DEFAULT_GOAL = help

# --------------------------------------------------------------------------- #
# Python version
PYTHON = python3
# Directory where scripts are saved
SRC_DIR = src
# Directory where binaries are saved
BIN_DIR = bin
# Directory where result files are saved
OUT_DIR = out

# Directory where the perf command is located
PERF = /usr/bin/perf
# Directory where the script toplev.py command is located
# TODO: change the next PATH with your own!
TLEV = /home/jlpadillas01/pmu-tools/toplev.py
# TLGRAPH = /home/jlpadillas01/pmu-tools/tl-barplot.py
# Basta con anhadir --graph a tlev para que se repsente el resultado en una grafica

# Events we want to measure with perf
# Portatil:
# EVENTS = instructions,cycles,fp_arith_inst_retired.128b_packed_double,fp_arith_inst_retired.128b_packed_single,fp_arith_inst_retired.256b_packed_double,fp_arith_inst_retired.256b_packed_single,fp_arith_inst_retired.scalar_double,fp_arith_inst_retired.scalar_single,fp_assist.any
# Sobremesa:
EVENTS = instructions,cycles,fp_assist.simd_input,fp_assist.simd_output,fp_assist.x87_input,fp_assist.x87_output,fp_comp_ops_exe.sse_packed_double,fp_comp_ops_exe.sse_packed_single,fp_comp_ops_exe.sse_scalar_double,fp_comp_ops_exe.sse_scalar_single,fp_comp_ops_exe.x87,simd_fp_256.packed_double,simd_fp_256.packed_single,arith.fpu_div,arith.fpu_div_active

# --------------------------------------------------------------------------- #
# Example
square:
	gcc -Wall -Werror -fPIC -I./src/ -c src/square.c -o bin/square.o
	gcc -shared -o libsquare.so bin/square.o

cube:
	gcc -Wall -Werror -fPIC -I./src/ -c src/cube.c -o bin/cube.o
	gcc -shared -o libcube.so bin/cube.o

main:
	# Compile
	gcc -Wall -Werror -I./src/ -c src/main.c -o bin/main.o
	# Link
	gcc -o prog bin/main.o -L. -lcube -lsquare -lm

# --------------------------------------------------------------------------- #
# my_papi
my_papi:
	gcc -Wall -Werror -fPIC -I./src/ -c src/my_papi.c -o bin/my_papi.o
	gcc -shared -o libmy_papi.so bin/my_papi.o -L/usr/local/lib -lpapi

	gcc -Wall -Werror -I./src/ -c src/papi_main.c -o bin/papi_main.o
	gcc -o papi_prog bin/papi_main.o -L. -lmy_papi
	
	# Importante! de lo contrario no nos deja de medir la 1a vez
	sudo sysctl -w kernel.perf_event_paranoid=1
	export LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:.:/usr/local/lib
	./papi_prog

papi_main:
	# Compile
	gcc -Wall -Werror -I./src/ -c src/papi_main.c -o bin/papi_main.o
	# Link
	gcc -o papi_prog bin/papi_main.o -L. -lmy_papi -lm

clean:
	rm bin/* *.so *prog
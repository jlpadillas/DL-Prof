# --------------------------------------------------------------------------- #
# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help setup clean

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
EVENTS = instructions,cycles,fp_arith_inst_retired.128b_packed_double,fp_arith_inst_retired.128b_packed_single,fp_arith_inst_retired.256b_packed_double,fp_arith_inst_retired.256b_packed_single,fp_arith_inst_retired.scalar_double,fp_arith_inst_retired.scalar_single,fp_assist.any
# --------------------------------------------------------------------------- #

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To execute the python script with perf type 'make perf'"
	@echo "To execute the python script with tlev type 'make tlev'"
	@echo "To clean the binaries/results type 'make clean'"
	@echo "------------------------------------"

# This generates the desired project file structure
# A very important thing to note is that macros (or makefile variables) are referenced in the target's code with a single dollar sign ${},
# but all script variables are referenced with two dollar signs $${}
setup:	
	@echo "Checking if project files are generated..."
	[ -d bin ] || (echo "No directory found, generating..." && mkdir bin)
	# for FILE in ${FILES}; do \
	# 	touch "project_files.project/$${FILE}.txt"; \
	# done

perf:
	sudo sysctl -w kernel.nmi_watchdog=0
	sudo ${PERF} stat --event ${EVENTS} --cpu=0 taskset -c 0 ${PYTHON} ${SRC_DIR}/mat_mul.py
	sudo ${PERF} stat --event ${EVENTS} --cpu=0 taskset -c 0 ${PYTHON} ${SRC_DIR}/mat_mul_zeros.py
	sudo sysctl -w kernel.nmi_watchdog=1

tlev:
	sudo sysctl -w kernel.nmi_watchdog=0
	sudo ${TLEV} --core C0 -l4 --no-desc --raw taskset -c 0 ${PYTHON} ${SRC_DIR}/mat_mul.py
	# sudo ${TLEV} --core C0 -l4 --no-desc taskset -c 0 ${PYTHON} ${SRC_DIR}/mat_mul_zeros.py
	sudo sysctl -w kernel.nmi_watchdog=1

clean:
	rm -r bin

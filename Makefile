# Python version
PYTHON = python3

# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help setup test run clean

# Defining an array variable
FILES = input output

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To setup the project type make setup"
	@echo "To test the project type make test"
	@echo "To run the project type make run"
	@echo "------------------------------------"

# This generates the desired project file structure
# A very important thing to note is that macros (or makefile variables) are referenced in the target's code with a single dollar sign ${},
# but all script variables are referenced with two dollar signs $${}
setup:	
	@echo "Checking if project files are generated..."
	[ -d project_files.project ] || (echo "No directory found, generating..." && mkdir project_files.project)
	for FILE in ${FILES}; do \
		touch "project_files.project/$${FILE}.txt"; \
	done

test:
	${PYTHON} -m pytest

run:
	${PYTHON} our_app.py

clean:
	rm -r *.project
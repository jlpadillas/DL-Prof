#!/bin/bash

CC=$(which python3)
SRC_DIR="src"
# program="mnist_papi.py"
program="mnist_train_callback.py"
# program="mnist_each_epoch.py"
num_executions=5

for (( i = 0; i < num_executions; i++ )); do
    eval taskset -c 2 "$CC" "${SRC_DIR}/${program}"
done

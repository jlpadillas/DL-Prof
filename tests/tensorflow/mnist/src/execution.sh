#!/bin/bash

CC=$(which python3)
SRC_DIR="src"
# program="mnist_papi.py"
# program="mnist_train_callback.py"
# program="mnist_each_epoch.py"
# program="mnist_each_batch.py"
declare -a programs=( "mnist_papi.py" "mnist_train_callback.py" "mnist_each_epoch.py" "mnist_each_batch.py")

num_executions=5

for prog in "${programs[@]}"; do
    for (( i = 0; i < num_executions; i++ )); do
        eval taskset -c 2-31 "$CC" "${SRC_DIR}/${prog}"
    done
done

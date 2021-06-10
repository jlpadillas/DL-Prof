#!/bin/bash

CC=$(which python3)
# SRC_DIR="src"
SRC_DIR="/afs/atc.unican.es/u/j/juan/PAPI-for-python-and-tf2/tests/tensorflow/fashion-mnist/src"

# Creates the output folder
OUT_DIR="/afs/atc.unican.es/u/j/juan/PAPI-for-python-and-tf2/tests/tensorflow/fashion-mnist/out"
# mkdir -p ${OUT_DIR}

# File where stdout and stderr content will be stored
output_file="${OUT_DIR}/execution.txt"

# program="mnist_papi.py"
# program="mnist_train_callback.py"
# program="mnist_each_epoch.py"
# program="mnist_each_batch.py"
# declare -a programs=( "mnist_papi.py" "mnist_train_callback.py" "mnist_each_epoch.py" "mnist_each_batch.py")
declare -a programs=( "mnist_train_callback.py" )

declare -a inter_list=( 0 1 )
declare -a intra_list=( 0 1 2 16 32 )

num_executions=3

for prog in "${programs[@]}"; do
    for inter in "${inter_list[@]}"; do
        for intra in "${intra_list[@]}"; do
            for (( i = 0; i < num_executions; i++ )); do
                time eval taskset -c 2-31 "$CC" "${SRC_DIR}/${prog}" "${inter}" "${intra}" \
                    "${OUT_DIR}/taskset-2-31_inter-${inter}_intra-${intra}.csv" &>> "${output_file}"
            done
        done
    done
done

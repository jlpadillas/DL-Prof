#!/bin/bash

CC=$(which python3)

# Define the directories/path to the files
HOME_DIR="/afs/atc.unican.es/u/j/juan"
MNIST_DIR="${HOME_DIR}/models/official/vision/image_classification"
OUT_DIR="${HOME_DIR}/mnist_out"
# Creates the output folder
mkdir -p ${OUT_DIR}

# Set the program to execute
PROGRAM="${MNIST_DIR}/mnist_main.py"

# File where stdout and stderr content will be stored
STDERR_FILE="${OUT_DIR}/matmul.stderr"
TIME_FILE="${OUT_DIR}/time.txt"
# OUTPUT_FILE="${OUT_DIR}/execution.csv"

# Now, we can define the params to pass to the program
MODEL_DIR="${HOME_DIR}/model_dir"
DATA_DIR="${HOME_DIR}/data_dir"

# And set the number of executions to perform
NUM_EXECUTIONS=10

# Define the list of batch size to measure
#declare -a batch_size_list=( 1 2 4 8 16 32 64 128 256 512 )
#declare -a batch_size_list=( 16284 8192 4096 2048 1024 512 256 128 64 32 16 8 4 2 1 )
declare -a batch_size_list=( 60000 10000 6000 1000 600 100 60 32 16 8 4 2 1 )


for batch_size in "${batch_size_list[@]}"; do
    for (( i = 0; i < NUM_EXECUTIONS; i++ )); do

        printf '\nStarting measure of batch_size:\t%s\t%s\n' "$batch_size" "$i"

        { time \
            eval taskset -c 2-31 "${CC}" "${PROGRAM}" "${OUT_DIR}/Ex3_mnist_B-${batch_size}.csv" "$batch_size" \
            --model_dir="$MODEL_DIR" --data_dir="$DATA_DIR" --train_epochs=1 --distribution_strategy=one_device \
            2>> "${STDERR_FILE}" ; } 2>> "${TIME_FILE}"
    done
done
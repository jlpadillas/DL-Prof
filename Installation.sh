#!/bin/bash

# Se necesitan los siguientes paquetes para ejecutar nuestro programa

sudo apt-get update
sudo apt-get upgrade -y

# gcc
sudo apt install build-essential manpages-dev -y

# git
sudo apt install git -y

# ----
# PAPI
cd ~ || exit
git clone https://bitbucket.org/icl/papi.git
cd papi || exit
git pull https://bitbucket.org/icl/papi.git

# Install in linux
cd src || exit

sudo sysctl -w kernel.nmi_watchdog=0 > /dev/null # Disable NMI
sudo sysctl -w kernel.perf_event_paranoid=0 > /dev/null # Allow perf measure
sudo ./configure
sudo make
# make test
# make fulltest
# ./run_tests.sh -v
sudo sysctl -w kernel.perf_event_paranoid=4 > /dev/null # Back to normal
sudo sysctl -w kernel.nmi_watchdog=1 > /dev/null # Enable NMI
sudo make install-all

# ----
# PERF
sudo apt install linux-tools-common linux-tools-generic \
    linux-tools-"$(uname -r)" -y

# ----
# CREATING VIRTUAL ENVIRON.
# 
# Create a general folder in home
cd ~ || exit
mkdir -p Environments
cd Environments || exit

# Inside, create a virtualenv
virtualenv -p /usr/bin/python3 py3_tensorflow_env

# Activates it
source py3_tensorflow_env/bin/activate

# Install dependencies
pip install matplotlib numpy pandas scipy scikit-learn dash
# ! tensorflow
pip install tensorflow
# ! tensorflow with AVX512
pip install https://storage.googleapis.com/intel-optimized-tensorflow/2.3.0/intel_tensorflow_avx512-2.3.0-cp37-cp37m-manylinux2010_x86_64.whl
# ! Para instalar los datasets que hay en model garden
pip install tensorflow-datasets

# Deactivate it
deactivate

# ! To remove the env
# rm -rf py3_tensorflow_env/
#!/usr/bin/env bash

# Se carga el PATH -> IMPORTANTE!
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./lib:/usr/local/lib

# --------------------------------------------------------------------------- #
# Carpeta donde se encuentran los ejecutables
BIN_DIR=bin
# Carpeta donde se encuentran las librerias generadas
LIB_DIR=lib
# Carpeta donde se vuelcan los datos de salida
OUT_DIR=out
# Carpeta donde se encuentran los archivos fuente
SRC_DIR=src

# Se crean los directorios en caso de no existir
mkdir -p $BIN_DIR $OUT_DIR
# Se elimina y se vuelve a crear el log
FILE=$OUT_DIR/results1.log
if [ -f $FILE ]; then
  rm $FILE
fi
touch $FILE
# --------------------------------------------------------------------------- #
# Flags used to compile c files
CFLAGS="-Wall -Werror"
CC=$(which gcc)
INCLUDE=-I./${SRC_DIR}

# Programa con el que mediremos el tiempo de ejecucion
# EXE=/usr/bin/time

# Se definen las CPUs con las que se prueba
# NUM_CPUS=( 2 4 6 8 10 )

# Datos a pasar como parametros
# DATA_A=-50.9
# DATA_B=60.3
# DATA_N=1000000

# Formato de salida del comando time
# FORMAT='\t\t\t%U\t%S\t%E\t\t%P'

make clean >/dev/null

# --------------------------------------------------------------------------- #
# C
# --------------------------------------------------------------------------- #
# Se mide main.c para PERF y para PAPI (my_papi)

# Se compilan los programas
# ! matrix
eval "${CC}" "${CFLAGS}" -c -pthread ${SRC_DIR}/matrix.c -o ${BIN_DIR}/matrix
# ! my_papi
eval "${CC}" "${CFLAGS}" -c -fPIC ${INCLUDE} ${SRC_DIR}/my_papi.c -o \
  ${BIN_DIR}/my_papi.o
eval "${CC}" -shared -L/usr/local/lib -lpapi ${BIN_DIR}/my_papi.o -o \
  "${LIB_DIR}"/libmy_papi.so
# ? main
eval "${CC}" "${CFLAGS}" -pthread $SRC_DIR/main.c ${BIN_DIR}/matrix -o \
  ${BIN_DIR}/main
# ? main_papi
eval "${CC}" "${CFLAGS}" ${INCLUDE} -c ${SRC_DIR}/main.c -DMY_PAPI -o \
  ${BIN_DIR}/main_papi.o

eval "${CC}" "${CFLAGS}" -pthread ${BIN_DIR}/matrix ${BIN_DIR}/main_papi.o  \
  -L${LIB_DIR} -lmy_papi -o ${BIN_DIR}/main_papi -lpapi


sudo sysctl -w kernel.nmi_watchdog=0 > /dev/null
sudo sysctl -w kernel.perf_event_paranoid=-1 > /dev/null
./${BIN_DIR}/main_papi RAND 500 NORMAL
sudo sysctl -w kernel.perf_event_paranoid=4 > /dev/null
sudo sysctl -w kernel.nmi_watchdog=1 > /dev/null


# # Empieza la ejecucion
# printf "CPU:" >> $FILE
# ./${BIN_DIR}/main RAND 500 NORMAL
# for NP in "${NUM_CPUS[@]}"
# do
#   printf " $NP" >> $FILE
# done
# printf "\n\t\t\tUser\tSystem\tElapsed\t%%CPU\n" >> $FILE
# # 2 estaciones de prueba
# for season in 1 2
# do
#   printf "\tSeason: $season\n" >> $FILE # numero de season
#   program=trap_sec
#   printf "\t\t$program : \n" >> $FILE
#   for i in `seq 1 1 11`; # 11 = 10 + 1 de warm-up
#   do
#     $EXE --format $FORMAT -o $FILE --append $BIN/$program $DATA_A $DATA_B $DATA_N # results dumped
#     sleep 1
#   done
# done


# # Empieza la ejecucion con un bucle que varia el num de CPUs
# for NP in "${NUM_CPUS[@]}"
# do
#   printf "CPU: $NP\n" >> $FILE
#   printf "\t\t\tUser\tSystem\tElapsed\t%%CPU\n" >> $FILE
#   # 2 estaciones de prueba
#   for season in 1 2
#   do
#     printf "\tSeason: $season\n" >> $FILE # numero de season
#     program=trap_th
#     printf "\t\t$program : \n" >> $FILE
#     for i in `seq 1 1 11`; # 11 = 10 + 1 de warm-up
#     do
#       $EXE --format $FORMAT -o $FILE --append $BIN/$program $DATA_A $DATA_B $DATA_N $NP # results dumped
#       sleep 1
#     done

#     # Para ejecutar el programa con mpi se necesita un comando y no el ./
#     program=trap_mpi
#     printf "\t\t$program : \n" >> $FILE
#     for i in `seq 1 1 11`; # 11 = 10 + 1 de warm-up
#       do
#         $EXE --format $FORMAT -o $FILE --append mpirun --oversubscribe --mca btl_vader_single_copy_mechanism \
#         none -np $NP $BIN/$program $DATA_A $DATA_B $DATA_N # results dumped
#         sleep 1
#       done
#   done
#   printf " ------------------------------------------------------------ \n" >> $FILE
# done
# printf "END of execution.sh" >> $FILE
# echo "done"
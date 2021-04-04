#!/usr/bin/env bash

# Se compilan los archivos llamando al Makefile
make compile

# Se elimina y se vuelve a crear el log
FILE=results1.log
if [ -f $FILE ]; then
  rm $FILE
fi
touch $FILE

# Programa con el que mediremos el tiempo de ejecucion
EXE=/usr/bin/time

# Carpeta donde se encuentran los ejecutables
BIN=./bin

# Se definen las CPUs con las que se prueba
NUM_CPUS=( 2 4 6 8 10 )

# Datos a pasar como parametros
DATA_A=-50.9
DATA_B=60.3
DATA_N=1000000

# Solucion: 52_273.9

# Formato de salida del comando time
FORMAT='\t\t\t%U\t%S\t%E\t\t%P'

# Empieza la UNICA ejecucion del modo secuencial porque, independientemente
# de los CPUs que se usen, el tiempo sera el mismo y no variara su tiempo de
# ejecucion
printf "CPU:" >> $FILE
for NP in "${NUM_CPUS[@]}"
do
  printf " $NP" >> $FILE
done
printf "\n\t\t\tUser\tSystem\tElapsed\t%%CPU\n" >> $FILE
# 2 estaciones de prueba
for season in 1 2
do
  printf "\tSeason: $season\n" >> $FILE # numero de season
  program=trap_sec
  printf "\t\t$program : \n" >> $FILE
  for i in `seq 1 1 11`; # 11 = 10 + 1 de warm-up
  do
    $EXE --format $FORMAT -o $FILE --append $BIN/$program $DATA_A $DATA_B $DATA_N # results dumped
    sleep 1
  done
done


# Empieza la ejecucion con un bucle que varia el num de CPUs
for NP in "${NUM_CPUS[@]}"
do
  printf "CPU: $NP\n" >> $FILE
  printf "\t\t\tUser\tSystem\tElapsed\t%%CPU\n" >> $FILE
  # 2 estaciones de prueba
  for season in 1 2
  do
    printf "\tSeason: $season\n" >> $FILE # numero de season
    program=trap_th
    printf "\t\t$program : \n" >> $FILE
    for i in `seq 1 1 11`; # 11 = 10 + 1 de warm-up
    do
      $EXE --format $FORMAT -o $FILE --append $BIN/$program $DATA_A $DATA_B $DATA_N $NP # results dumped
      sleep 1
    done

    # Para ejecutar el programa con mpi se necesita un comando y no el ./
    program=trap_mpi
    printf "\t\t$program : \n" >> $FILE
    for i in `seq 1 1 11`; # 11 = 10 + 1 de warm-up
      do
        $EXE --format $FORMAT -o $FILE --append mpirun --oversubscribe --mca btl_vader_single_copy_mechanism \
        none -np $NP $BIN/$program $DATA_A $DATA_B $DATA_N # results dumped
        sleep 1
      done
  done
  printf " ------------------------------------------------------------ \n" >> $FILE
done
printf "END of execution.sh" >> $FILE
echo "done"
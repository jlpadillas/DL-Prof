#!/usr/bin/env bash

# --------------------------------------------------------------------------- #
# Functions
# --------------------------------------------------------------------------- #
set_environment () {
# Fija la frecuencia del CPU a una pasada por parametro y desactiva el
# turbo-boost mediante el uso de los registros msr. Si no se pasa una
# frecuencia, se fija por defecto a 2.2GHz. Formato de la frecuencia
# permitida: 800MHz, 1.9GHz, etc.
# Note. Necesario tener instalado el paquete 'msr-tools'
  # Se fija la frecuencia de la CPU
  local FREQ=2.2GHz
  local MSR="0x1a0"
  local CODE="0x4000850089"
  # Carga libreria para hacer cambios en los registros msr
  sudo modprobe msr
  # Se deshabilita el turboboost de Intel
  sudo wrmsr --all $MSR $CODE
  # Establece el governor del CPU
  sudo cpupower frequency-set --governor userspace
  # Establece la frecuencia del CPU
  sudo cpupower frequency-set --freq $FREQ
}

# --------------------------------------------------------------------------- #
# Params
# --------------------------------------------------------------------------- #
# Ruta hasta el directorio actual
PWD=$(pwd)
# Carpeta donde se encuentran los ejecutables
BIN_DIR=$PWD/bin
# Carpeta donde se encuentran las librerias generadas
LIB_DIR=$PWD/lib
# Carpeta donde se vuelcan los datos de salida
OUT_DIR=$PWD/out
# Carpeta donde se encuentran los archivos fuente
SRC_DIR=$PWD/src

# ! Se eliminan los archivos antiguos! IMPORTANTE
rm -rf "${BIN_DIR:?}/"* "${LIB_DIR:?}/"* >/dev/null

# Se crean los directorios en caso de no existir
mkdir -p "$BIN_DIR" "$LIB_DIR" "$OUT_DIR"
# Se elimina y se vuelve a crear el log
FILE=$OUT_DIR/results1.log
if [ -f "$FILE" ]; then
  rm "$FILE"
fi
touch "$FILE"

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


# --------------------------------------------------------------------------- #
# C
# --------------------------------------------------------------------------- #
# Flags used to compile c files
CFLAGS="-Wall -Werror"
CC=$(which gcc)
# Se compilan los programas
# ! matrix
eval "${CC}" "${CFLAGS}" "${SRC_DIR}"/matrix.c -c -o "${BIN_DIR}"/matrix.o
# ! main
eval "${CC}" "${CFLAGS}" "$SRC_DIR"/main.c "${BIN_DIR}"/matrix.o -pthread -o \
  "${BIN_DIR}"/main
# ! my_papi
eval "${CC}" "${CFLAGS}" -fPIC -c "${SRC_DIR}"/my_papi.c -o \
  "${BIN_DIR}"/my_papi.o
eval "${CC}" -shared -o "${LIB_DIR}"/libmy_papi.so "${BIN_DIR}"/my_papi.o \
  -L/usr/local/lib -lpapi
# ! main_papi
eval "${CC}" "${CFLAGS}" "${SRC_DIR}"/main.c -o "${BIN_DIR}"/main_papi \
  -DMY_PAPI -Wl,-rpath="$LIB_DIR" "${BIN_DIR}"/matrix.o -L"${LIB_DIR}" \
  -lmy_papi -pthread

# TODO: Se carga el PATH -> IMPORTANTE!
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$PWD:/usr/local/lib
# echo "$LD_LIBRARY_PATH"

# --------------------------------------------------------------------------- #
# Se mide main.c para PERF y para PAPI (my_papi)
# --------------------------------------------------------------------------- #
# Definimos las matrices a ejecutar
# declare -a M_TYPE=( "RAND" "SEQ" )
declare -a M_TYPE=( "SEQ" )
# declare -a M_SIZE=( 1024 10240 )
declare -a M_SIZE=( 512 )
# declare -a M_MULT=( "MULTITHREAD" "NORMAL" "TRANSPOSE" )
declare -a M_MULT=( "NORMAL" )

# ./bin/main SEQ 512 NORMAL

# Empieza la ejecucion de los programas
for m_type in "${M_TYPE[@]}"; do
  # Tipo de matriz: RANDO o SEQUENTIAL
  printf " ======================================================= \n" >> "$FILE"
  printf "[%s]\n" "$m_type" >> "$FILE"

  for m_size in "${M_SIZE[@]}"; do
    # Tamanho de la matriz: 1024, ..., 10240
    printf " -------------------------------------------------- \n" >> "$FILE"
    printf "\t[%s]\n" "$m_size" >> "$FILE"

    for m_mult in "${M_MULT[@]}"; do
      # Tipo de multiplicacion a realizar: multithread, normal, transpose, ...
      printf " _____________________________________________ \n" >> "$FILE"
      printf "\t\t[%s]\n" "$m_mult" >> "$FILE"

      # for program in "main_papi" "main"; do
      for program in "main" "main_papi"; do
        printf "\t\t\tProgram: %s\n" "$program" >> "$FILE"
        
        for season in 1 2; do
          # 2 estaciones de prueba
          printf "\tSeason: %s\n" "$season" >> "$FILE" # numero de season
          for (( i = 1; i <= 3; i++ )); do # 3 = 2 + 1 de warm-up

            if [[ $program == *"papi"* ]]; then
              eval bash "${SRC_DIR}/"perf.sh --papi "${BIN_DIR}/"${program} \
                "$m_type" "$m_size" "$m_mult" >> "$FILE" 2>&1
            else
              eval bash "${SRC_DIR}/"perf.sh "${BIN_DIR}/"${program} \
                "$m_type" "$m_size" "$m_mult" >> "$FILE" 2>&1
            fi

            sleep 1
          done
        done

      done
      printf " _____________________________________________ \n" >> "$FILE"
    done
    printf " -------------------------------------------------- \n" >> "$FILE"
  done
  printf " ======================================================= \n" >> "$FILE"
done


# ./${BIN_DIR}/main_papi RAND 500 NORMAL



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
#!/usr/bin/env bash


# Starting program...
start=$(date +%s)

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

format () {
# The fields are in this order:
# •   optional usec time stamp in fractions of second (with -I xxx)
# •   optional CPU, core, or socket identifier
# •   optional number of logical CPUs aggregated
# •   counter value
# •   unit of the counter value or empty
# •   event name
# •   run time of counter
# •   percentage of measurement time the counter was running
# •   optional variance if multiple values are collected with -r
# •   optional metric value
# •   optional unit of metric
# Additional metrics may be printed with all earlier fields being empty.

  # Se separa el contenido para leerlo
  readarray -t array <<< "$1"
  printf "%s\n" "+---------------------------------------+-----------------+"
  printf "| %-38s| %-16s|\n" "Event" "Value"
  printf "%s\n" "+---------------------------------------+-----------------+"
  for line in "${array[@]}"; do
    readarray -td: data <<< "$line"
    local counter_val="${data[0]}"
    local event_name="${data[2]}"
    if [[ $counter_val -ne 0 ]]; then
      printf "| %-38s| %'-16lld|\n" "${event_name}" "${counter_val}"
    fi
  done
  printf "%s\n" "+---------------------------------------+-----------------+"
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
declare -a M_MULT=( "TRANSPOSE" "MULTITHREAD")

declare -a TASKSET=( "YES" "NO")

{
  for m_type in "${M_TYPE[@]}"; do
    # Tipo de matriz: RANDOM o SEQUENTIAL

    for m_size in "${M_SIZE[@]}"; do
      # Tamanho de la matriz: 1024, ..., 10240

      for m_mult in "${M_MULT[@]}"; do
        # Tipo de multiplicacion a realizar: multithread, normal, transpose, ...

        for program in "main" "main_papi"; do

printf "\n%s\n" "+=============+=============+========================+===========+"
printf "|%+12s |%+12s |%+23s |%+10s |\n" "MATRIX TYPE" "MATRIX SIZE" \
  "TYPE OF MULTIPLICATION" "PROGRAM"
printf "%s\n" "+=============+=============+========================+===========+"
printf "|%+12s |%+12s |%+23s |%+10s |\n" "$m_type" "$m_size" "$m_mult" "$program"
printf "%s\n" "+=============+=============+========================+===========+"

# TODO: Falta anhadir el parametro taskset. Comprobar que el multithread funciona
# TODO: PAPI No mide bien multithread sin taskset

          for season in 1 2; do
            # 2 estaciones de prueba

            printf "\n\tSeason: %s\n\n" "$season" # numero de season
            for (( i = 1; i <= 3; i++ )); do # 3 = 2 + 1 de warm-up

              if [[ $program == *"papi"* ]]; then
                eval bash "${SRC_DIR}/"perf.sh --papi "${BIN_DIR}/"${program} \
                  "$m_type" "$m_size" "$m_mult" 2>&1
              else
                AUX=$(eval bash "${SRC_DIR}/"perf.sh "${BIN_DIR}/"${program} \
                  "$m_type" "$m_size" "$m_mult" 2>&1)
                format "$AUX"
              fi

              sleep 1
            done
          done

        done
      done
    done
  done
  printf "\nEOF\n"
} >> "$FILE"

# Ending program!
end=$(date +%s)
echo "Execution time was $(("$end" - "$start")) seconds."
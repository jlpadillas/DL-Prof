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




# With -x, perf stat is able to output a not-quite-CSV format output Commas in the output are not put into "".
# To make it easy to parse it is recommended to use a different character like -x \;

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

# ---------------------------------------------

# 3449195817::instructions:221979762:35,75:1:insn per cycle
# 2242014845::cycles:267154596:43,02::
# 0::fp_assist.any:270837981:43,62::
# 0::fp_assist.simd_input:270907525:43,63::
# 0::fp_assist.simd_output:270989133:43,64::
# 0::fp_assist.x87_input:270978093:43,64::
# 0::fp_assist.x87_output:175061758:28,19::
# 0::fp_comp_ops_exe.sse_packed_double:175027661:28,19::
# 0::fp_comp_ops_exe.sse_packed_single:175098694:28,20::
# 663358917::fp_comp_ops_exe.sse_scalar_double:174921480:28,17::
# 0::fp_comp_ops_exe.sse_scalar_single:175051892:28,19::
# 14645::fp_comp_ops_exe.x87:175016445:28,19::
# 0::simd_fp_256.packed_double:174863804:28,16::
# 0::simd_fp_256.packed_single:175052058:28,19::


format () {
  # Se guardan los parametros en var. locales
  local STR=$1
  local FILE=$2
  # Se separa el contenido para leerlo
  echo "$STR" | 
  readarray -t array <<< "$STR"

  declare -p array

  echo "$array"



  # DATA=$(echo "$STR" | tr ' ' '-') # array w 1 element

  # IFS=', ' read -r -a array <<< "$DATA"

  # readarray -td, a <<<"$DATA,"; declare -p a;

  # readarray -td, a <<<"$STR\n"; unset 'a[-1]'; declare -p a;
  # readarray -td '' a < <(awk '{ gsub(/, /,"\0"); print; }' <<<"$STR,"); unset 'a[-1]';
  # declare -p a;


  # echo "${#a[@]}" "SIUUUUUUUU"


  # readarray -td '' a < <(awk '{ gsub(/, /,"\0"); print; }' <<<"$string, "); unset 'a[-1]';
  # declare -p a;
  # ## declare -a a=([0]="Paris" [1]="France" [2]="Europe")



  # function mfcb { local val="$4"; "$1"; eval "$2[$3]=\$val;"; };
  # function val_ltrim { if [[ "$val" =~ ^[[:space:]]+ ]]; then val="${val:${#BASH_REMATCH[0]}}"; fi; };
  # function val_rtrim { if [[ "$val" =~ [[:space:]]+$ ]]; then val="${val:0:${#val}-${#BASH_REMATCH[0]}}"; fi; };
  # function val_trim { val_ltrim; val_rtrim; };
  # readarray -c1 -C 'mfcb val_trim a' -td, <<<"$STR,"; unset 'a[-1]'; declare -p a;
  # declare -a a=([0]="Paris" [1]="France" [2]="Europe")


  # echo "Hola %s" "${a[14]}"


  # | tr ':' '\n'
  # declare -a DATA=$DATA
  # eval echo "$STR" | tr ':' '\t' >> "$FILE" 2>&1


  # lines=$(echo "$DATA" | tr ':' '\n')

  # # echo "${lines[0]}"


  # echo "${#lines[@]}" "SIUUUUUUUU"

  # for i in "${DATA[@]}"; do
  # # for line in "${DATA[@]}"; do

  #   # echo "$i"
  #   printf "%s <- end\n" "$i[0]"
  #   # echo "$line[0] ---"

  #   # for j in $i; do
  #   #   LINE=$(echo "$j" | tr ':' '\n')
  #   #   L_0=${i[0]}
  #   #   L_1=${LINE[1]}
  #   #   L_2=${LINE[2]}
  #   #   L_3=${i[3]}
  #   #   # L_4=${LINE[4]}
  #   #   # L_5=${LINE[5]}
  #   #   # L_6=${LINE[6]}
  #   #   # for k in "${LINE[@]}"; do
  #   #   #   printf "%s" "$k"
  #   #   #   # echo "$j"
  #   #   #   printf "\n"
  #   #   # done

  #   #   echo "$L_0 - $L_3" >> "$FILE" 2>&1
  #   # done
  
  
  # done

  # echo "${DATA[0]}" >> "$FILE" 2>&1
  # echo "$DATA" >> "$FILE" 2>&1
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
              CASA=$(eval bash "${SRC_DIR}/"perf.sh "${BIN_DIR}/"${program} \
                "$m_type" "$m_size" "$m_mult" 2>&1)
              format "$CASA" "$FILE"
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

# Ending program!
end=$(date +%s)
echo "Execution time was $(("$end" - "$start")) seconds."
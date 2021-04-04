#!/usr/bin/env bash

# Se carga el PATH -> IMPORTANTE!
export PATH=$PATH:/usr/local/cuda/bin

# Carpeta donde se encuentran los programas
SRC=./src

# Carpeta donde se encuentran los ejecutables
BIN=./bin

# Carpeta donde se encuentran las imagenes
ANX=./Anexo

# Carpeta donde se crearan las imagenes de salida
DST=./out
mkdir -p $BIN
mkdir -p $DST

# Definimos los programas a ejecutar
# declare -a PROGRAMS=( "codigoBase_CUDA_v1" )
# declare -a PROGRAMS=( "codigoBase" "codigoBase_CUDA_v0" )
declare -a PROGRAMS=( "codigoBase" "codigoBase_CUDA_v0" "codigoBase_CUDA_v1" )

# Imagenes a pasar como parametros (formato .jpg)
# declare -a IMAGES=( "CampNou" )
# declare -a IMAGES=( "facultad" "Santander" )
declare -a IMAGES=( "facultad" "Santander" "CampNou" )

# Se compilan los programas llamando al compilador
for program in "${PROGRAMS[@]}"
do
  nvcc $SRC/"${program}.cu" -L/usr/lib/x86_64-linux-gnu -lopencv_highgui -lopencv_imgproc -o $BIN/$program $(pkg-config --libs --cflags opencv) -lm
done

# Programa con el que mediremos el tiempo de ejecucion
EXE=/usr/bin/time

# Formato de salida del comando time
#FORMAT='\t\t\t%U\t%S\t%E\t\t%P' # Usar sin CUDA_EVENT
#FORMAT='\t%U\t%S\t%E\t\t%P'

# Se elimina y se vuelve a crear el log
FILE=results.log
if [ -f $FILE ]; then
  rm $FILE
fi
touch $FILE

# Empieza la ejecucion de los programas
for program in "${PROGRAMS[@]}"
do
  printf "$program:\n" >> $FILE

  # Se ejecuta el programa para cada imagen
  for image in "${IMAGES[@]}"
  do
    printf "\t$image:\n" >> $FILE

    # 2 estaciones de prueba
    for season in 1 2
    do
      printf "\t\tSeason: $season\n" >> $FILE # numero de season
      if [[ $program = "codigoBase_CUDA_v1" ]]
      then
        FORMAT='\t%U\t%S\t%E\t\t%P'
        printf "\t\tKET(ms)\tUser\tSystem\tElapsed\t\t%%CPU\n" >> $FILE
      else
        FORMAT='\t\t\t%U\t%S\t%E\t\t%P' # Usar sin CUDA_EVENT
        printf "\t\t\tUser\tSystem\tElapsed\t\t%%CPU\n" >> $FILE # Usar sin CUDA_EVENT
      fi
      for i in `seq 1 1 3`; # 3 = 2 + 1 de warm-up
      do
        $EXE --format $FORMAT -o $FILE --append $BIN/$program "${ANX}/${image}.jpg" "${DST}/${image}_out_${program}_${season}_${i}.jpg">>$FILE # results dumped
        sleep 1
      done
    done
  done
  printf " ------------------------------------------------------------ \n" >> $FILE
done
printf "END of execution.sh\n" >> $FILE
echo "Done!"
# Deep-Learning sobre Hardware de propósito general, análisis de rendimiento basado en contadores hardware

Author: Juan Luis Padilla Salomé

Date: April 2021

---

## Interacción del código Python con contadores hardware

El objetivo de esta primera parte es comprobar que los contadores que se leen con PERF y con PAPI son similares.

Primero, se pretende medir los contadores hardware con un programa en C donde el resultado sea más o menos el esperado.  

Para ello, se ha decidido usar una multiplicación de matrices de punto flotante. La cual permitirá evitar gran parte del ruido que puede suponer el S.O. (y otros procesos) si se midiese instrucciones de enteros.

Se ha generado una "clase" llamada [matrix.c] que permite generar matrices de distintos tamaños y multiplicarlas aplicando distintos métodos. A partir de ésta, se ha creado un programa principal ([main.c]) con el cual podremos pasarle los parámetros y realizar mediciones sobre cuántas operaciones de punto flotante se realizan.





Se genera una clase [matrix.py]




[main.c]: 1.mat_mul/src/main.c
[matrix.c]: 1.mat_mul/src/matrix.c
[matrix.py]: 1.mat_mul/src/matrix.py
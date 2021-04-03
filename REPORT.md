# Deep-Learning sobre Hardware de propósito general, análisis de rendimiento basado en contadores hardware

Author: Juan Luis Padilla Salomé

Date: April 2021

---

## Interacción del código Python con contadores hardware

Primero, se pretende medir los contadores hardware con un programa en C donde el resultado sea más o menos el esperado.  

Para ello, se ha decidido usar una multiplicación de matrices de punto flotante. La cual permitirá evitar gran parte del ruido que puede suponer el S.O. (y otros procesos) si se mide instrucciones de enteros.

Se ha generado una "clase" llamada [matrix.c] que permite generar matrices de distintos tamaños y mutliplicarlas mediante distintas maneras.











Se genera una clase [matrix.py]




[matrix.c]: 1.mat_mul/src/matrix.c
[matrix.py]: 1.mat_mul/src/matrix.py
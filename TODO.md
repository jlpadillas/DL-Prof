# TODO

## Cosas a comentar

---

1. Reestructuración del repositorio. De 3 carpetas a 1. Se han unificado cosucas.

2. C -> Creado "objeto" [matrix.h]; y, un [main.c] que recibe por parámetro varias opciones para realizar la multip. de matrices.

3. Python -> Lo mismo ([main.py] y [matrix.py])

4. Librería [my_papi.h] se van anhadiendo más funciones útiles de PAPI.

5. Creado dos scripts:

   - [perf.sh] simula un perf pero, fijando un environment, midiendo eventos FP, habilitando permisos y midiendo tanto ejecutables (de C) como programas de python.

   - [execution.sh] realiza las ejecuciones y trata los datos para guardarlos en un fichero.

     - __DUDA__: las ejecuciones son variadas e igual renta hacer una media + std? _Comentar lo de las seasons y la ejecución de warm-up_.

---

## Lo interesante: ___multithread___

---

Mi [matrix.h] cuenta con 3 funciones para multiplicar matrices:

- ___mat_mul___ que multiplica "normal", variando sólo el orden de los índices de los fors (i, k, j).

- ___mat_mul_multithread___ que multiplica las matrices en paralelo (pthread).

- ___mat_mul_transpose___ utiliza la traspuesta de una matriz y que es más rápida que la "normal".

El resultado de ejecutar la traspuesta y el multithread es [abrir [results1_1.txt] y [results1_2.txt] en paralelo]

```text
+=============+=============+========================+===========+=========+
| MATRIX TYPE | MATRIX SIZE | TYPE OF MULTIPLICATION |   PROGRAM | TASKSET |
+=============+=============+========================+===========+=========+
|         SEQ |         512 |              TRANSPOSE |      main |      NO |
+=============+=============+========================+===========+=========+

	Season: 1

+---------------------------------------+-----------------+
| Event                                 | Value           |
+---------------------------------------+-----------------+
| instructions                          | 3.527.979.489   |
| cycles                                | 1.376.602.492   |
| fp_comp_ops_exe.sse_scalar_double     | 279.500.418     |
| fp_comp_ops_exe.x87                   | 5.793           |
+---------------------------------------+-----------------+
+---------------------------------------+-----------------+
| Event                                 | Value           |
+---------------------------------------+-----------------+
| instructions                          | 3.572.341.417   |
| cycles                                | 1.380.113.866   |
| fp_comp_ops_exe.sse_scalar_double     | 279.360.762     |
| fp_comp_ops_exe.x87                   | 5.973           |
+---------------------------------------+-----------------+
+---------------------------------------+-----------------+
| Event                                 | Value           |
+---------------------------------------+-----------------+
| instructions                          | 3.587.126.112   |
| cycles                                | 1.377.132.380   |
| fp_comp_ops_exe.sse_scalar_double     | 276.703.090     |
| fp_comp_ops_exe.x87                   | 8.577           |
+---------------------------------------+-----------------+

	Season: 2

+---------------------------------------+-----------------+
| Event                                 | Value           |
+---------------------------------------+-----------------+
| instructions                          | 3.645.644.216   |
| cycles                                | 1.472.456.552   |
| fp_comp_ops_exe.sse_scalar_double     | 264.301.539     |
| fp_comp_ops_exe.x87                   | 8.309           |
+---------------------------------------+-----------------+
+---------------------------------------+-----------------+
| Event                                 | Value           |
+---------------------------------------+-----------------+
| instructions                          | 3.613.708.922   |
| cycles                                | 1.404.520.648   |
| fp_comp_ops_exe.sse_scalar_double     | 283.102.944     |
| fp_comp_ops_exe.x87                   | 9.056           |
+---------------------------------------+-----------------+
+---------------------------------------+-----------------+
| Event                                 | Value           |
+---------------------------------------+-----------------+
| instructions                          | 3.528.503.108   |
| cycles                                | 1.392.407.921   |
| fp_comp_ops_exe.sse_scalar_double     | 282.153.980     |
| fp_comp_ops_exe.x87                   | 5.990           |
+---------------------------------------+-----------------+
```

---

attachar papi a un core. hace falta pasarle el úmero /numero de cores.

width/with

pasarle info a papi. de donde ejecuto mi tensorflow.

papi_cpu_attach ->mirar. granurality. tipo sistem.
papi options.
attach para cada core. mdir por separado.

0-2 y 4-6

attachment por core.

---

viernes 23-abr

makefile y python.

makefile  test.

libreria aparte. c q llama a papi

bash -> a python.

generar csv

tensorflow.

usable a modo usuario.

virtualenv.

---

[execution.sh]:   mat_mul/execution.sh
[main.c]:         mat_mul/src/main.c
[main.py]:        mat_mul/src/main.py
[matrix.h]:       mat_mul/src/matrix.h
[matrix.py]:      mat_mul/src/matrix.py
[my_papi.h]:      mat_mul/src/my_papi.h
[results1_1.txt]: mat_mul/out/results1_1.txt
[results1_2.txt]: mat_mul/out/results1_2.txt
[perf.sh]:        mat_mul/src/perf.sh

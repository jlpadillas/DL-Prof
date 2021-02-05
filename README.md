# TFG

## TODO:
Un ejemplo podría ser una multiplicación de matrices en punto flotante (que sean matrices gordas, para que dure un ratito, pero que no se te vaya la memoria). Prueba a medir contadores de los que puedas intuir o saber el resultado (número de instrucciones, aunque de este tendrás un valor aproximado, o número de instrucciones en punto flotante, que este tendrías que poder tener una mejor aproximación). Primero debes usar perf (o toplev) para medir estos contadores y ver que sale lo esperado. Cuando tengas esto, es momento de meterse en harina y hacer la medición mediante PAPI (invocando código C desde Python), y comprobar que te sale lo mismo que con perf.

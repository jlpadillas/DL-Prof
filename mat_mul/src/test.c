#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "my_papi.h"


int main(int argc, char const *argv[])
{
    int eventsets;
    int num_cpus = 1;
    char *file = "src/events_pc.cfg";
    // char *file = "src/events_node.cfg";
    // char *file = "src/events_laptop.cfg";
    my_prepare_measure(file, num_cpus, NULL, num_cpus, &eventsets);
    // my_prepare_measure(file, 1, NULL, 1, &eventsets);

    my_start_measure(1, &eventsets);
    printf("Hola\n");

    long long *m_values;
    my_stop_measure(num_cpus, &eventsets, &m_values);
    // for (i = 0; i < num_events; i++)
    // {
    //     printf("ev[%d]=%lld\n", i, (*values_local)[i]);
    // }
    // printf("valor = %lln\n", m_values);

    my_print_measure(num_cpus, NULL, &m_values, NULL);

    my_PAPI_shutdown();

    return 0;
}
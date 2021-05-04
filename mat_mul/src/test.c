#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "my_papi.h"


int main(int argc, char const *argv[])
{
    // -----------------------------------
    // char *file = "src/events_pc.cfg";
    // char *file = "src/events_node.cfg";
    char *file = "src/events_laptop.cfg";
    // -----------------------------------

    int *event_sets;
    int *cpus = NULL;
    int num_cpus;
    num_cpus = 1;
    num_cpus = my_get_total_cpus();
    int num_event_sets = num_cpus;

    event_sets = (int *)malloc(sizeof(int *) * num_cpus);

    my_prepare_measure(file, num_cpus, cpus, num_event_sets, event_sets);

    my_start_measure(num_event_sets, event_sets);
    
    printf("Soy el ROI\n");

    long long **values = (long long **)malloc(sizeof(long long **) * num_cpus);
    
    my_stop_measure(num_event_sets, event_sets, values);

    my_print_measure(num_cpus, NULL, values, NULL);

    my_PAPI_shutdown();

    return 0;
}
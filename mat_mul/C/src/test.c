#include <stdlib.h>
#include <stdio.h>
#include "my_papi.h"

int main(int argc, char const *argv[])
{
    // -----------------------------------
    // char *file = "conf/events_pc.cfg";
    // char *file = "conf/events_node.cfg";
    char *file = "conf/events_laptop.cfg";
    // -----------------------------------

    int *event_sets;
    int *cpus = NULL;
    int num_cpus;
    num_cpus = 1;
    num_cpus = my_get_total_cpus();
    int num_event_sets = num_cpus;
    char *output_file_name = "out/test.out.csv";

    event_sets = (int *)malloc(sizeof(int *) * num_cpus);

    my_prepare_measure(file, num_cpus, cpus, num_event_sets, event_sets);

    my_start_measure(num_event_sets, event_sets);

    // -----------------------
    // ROI
    printf("Soy el ROI\n");
    // -----------------------

    long long **values = (long long **)malloc(sizeof(long long **) * num_cpus);

    my_stop_measure(num_event_sets, event_sets, values);

    my_print_measure(num_cpus, cpus, values, output_file_name);

    my_free_measure(values, num_event_sets);

    my_PAPI_shutdown();

    return EXIT_SUCCESS;
}
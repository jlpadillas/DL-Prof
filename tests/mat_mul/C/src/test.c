#include <stdlib.h>
#include <stdio.h>
#include "my_papi.h"

int main(int argc, char const *argv[])
{
    // -------------------------------------------------------
    // char *file = "../../../my_papi/conf/events_pc.cfg";
    char *file = "../../../my_papi/conf/events_node.cfg";
    // char *file = "../../../my_papi/conf/events_laptop.cfg";
    // -------------------------------------------------------

    int *cpus = NULL;
    int num_cpus;
    num_cpus = 1;
    num_cpus = my_get_total_cpus();
    char *output_file_name = "out/test_out.csv";

    my_prepare_measure(file, num_cpus, cpus);

    my_start_measure();

    // -----------------------
    // ROI
    printf("Soy el ROI\n");
    // -----------------------

    my_stop_measure();

    my_print_measure(output_file_name);

    my_finalize_measure();

    return EXIT_SUCCESS;
}
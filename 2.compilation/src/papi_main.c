#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "../../1.mat_mul/src/matrix.h"
#include "my_papi.h"

int main(int argc, char const *argv[])
{
    /* Intializes random number generator */
    srand((unsigned)time(NULL));

    const unsigned dim_x_and_y = 700;
    const unsigned rows_a = dim_x_and_y;
    const unsigned cols_a = dim_x_and_y;
    const unsigned rows_b = dim_x_and_y;
    const unsigned cols_b = dim_x_and_y;

    // Reserve memory
    double *M_a = (double *)malloc(rows_a * cols_a * sizeof(double));
    double *M_b = (double *)malloc(rows_b * cols_b * sizeof(double));
    double *M_c = NULL;

    if (!M_a || !M_b)
    {
        fprintf(stderr, "Couldn't allocate memory!\n");
        exit(EXIT_FAILURE);
    }

    init_rand(M_a, rows_a, cols_a);
    init_rand(M_b, rows_b, cols_b);

    // EMPIEZA my_papi --------------------------------------------->
    // Rellenar por el "usuario":

    // portatil
    // const char *events[] = {
    //     "cycles",
    //     "instructions",
    //     "fp_arith_inst_retired.128b_packed_double",
    //     "fp_arith_inst_retired.128b_packed_single",
    //     // "fp_arith_inst_retired.256b_packed_double",
    //     // "fp_arith_inst_retired.256b_packed_single",
    //     "fp_arith_inst_retired.scalar_double",
    //     "fp_arith_inst_retired.scalar_single"
    //     // "fp_assist.any"
    // };

    // PC
    const char *events[] = {
        "cycles",
        "instructions",
        // "fp_assist.any",
        // "fp_assist.simd_input",
        // "fp_assist.simd_output",
        // "fp_assist.x87_input",
        // "fp_assist.x87_output",
        // "fp_comp_ops_exe.sse_packed_double",
        "fp_comp_ops_exe.sse_packed_single",
        "fp_comp_ops_exe.sse_scalar_double",
        // "fp_comp_ops_exe.sse_scalar_single", // no encuentra el evento!!!!!
        // "fp_comp_ops_exe.x87",
        "simd_fp_256.packed_double",
        "simd_fp_256.packed_single"
    };

    // NOTA: num. max. de eventos que puede medir papi simultaneamente
    // es igual a 6. Si se ejecuta mas, se lanza un error.
    const unsigned num_events = 6;
    long long *values = (long long *)malloc(num_events * sizeof(long long));

    int eventSet = my_start_events(events, num_events);

    // ROI -> Se multiplican
    M_c = mat_mul(M_a, rows_a, cols_a, M_b, rows_b, cols_b);

    my_stop_events(eventSet, num_events, values);

    for (int i = 0; i < num_events; i++)
    {
        printf("\tValue[%s]: %lld\n", events[i], values[i]);
    }

    // <----------------------------------------------- ACABA my_papi

    // printf("Matrix A: %s\n", arr_to_str(M_a, rows_a, cols_a));
    // printf("Matrix B: %s\n", arr_to_str(M_b, rows_b, cols_b));
    // printf("Matrix C: %s\n", arr_to_str(M_c, rows_a, cols_b));

    free(values);
    free(M_a);
    free(M_b);
    free(M_c);

    return EXIT_SUCCESS;
}
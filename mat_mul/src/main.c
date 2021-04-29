/** 
 * File:    main.c
 * 
 * Author:  Juan Luis Padilla Salome (juan-luis.padilla@alumnos.unican.es)
 * Date:    Spring 2021
 * 
 * Summary of File:
 * 
 *   This file contains code which executes a matrix multiplication.
 *   The main function allows to the user pass through parameters
 *   relative to how populate the matrix, the size and which method
 *   use to perform the multiplication.
 */

#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "matrix.h"

#ifdef MY_PAPI
#include "my_papi.h"
#endif // MY_PAPI

// #define MY_PAPI
// #define DEBUG
// #define RAW

#define MAX_MATRIX_SIZE 100000

#ifdef MY_PAPI
// ? NOTA: num. max. de eventos que puede medir papi simultaneamente
// ? es igual a 6. Si se ejecuta mas, se lanza un error.
const unsigned num_events = 3;

// ! Modify the next lines depending on the executing PC
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

// sobremesa
// const char *events[] = {
//     "cycles",
//     "instructions",
//     // "fp_assist.any",
//     // "fp_assist.simd_input",
//     // "fp_assist.simd_output",
//     // "fp_assist.x87_input",
//     // "fp_assist.x87_output",
//     // "fp_comp_ops_exe.sse_packed_double",
//     "fp_comp_ops_exe.sse_packed_single",
//     "fp_comp_ops_exe.sse_scalar_double",
//     // "fp_comp_ops_exe.sse_scalar_single", // no encuentra el evento!!!!!
//     "fp_comp_ops_exe.x87",
//     // "simd_fp_256.packed_double",
//     "simd_fp_256.packed_single"
// };

// NODO
const char *events[] = {
    "cycles",
    "instructions",
    // "fp_arith_inst_retired.128b_packed_double",
    // "fp_arith_inst_retired.128b_packed_single",
    // "fp_arith_inst_retired.256b_packed_double",
    // "fp_arith_inst_retired.256b_packed_single",
    // "fp_arith_inst_retired.512b_packed_double",
    // "fp_arith_inst_retired.512b_packed_single",
    "fp_arith_inst_retired.scalar_double",
    // "fp_arith_inst_retired.scalar_single"
    // "fp_assist.any"
};

#endif

enum MATRIX_TYPE
{
    RAND,
    SEQ
};

enum MULTIPLICATION_TYPE
{
    MULTITHREAD,
    NORMAL,
    TRANSPOSE
};

/** 
 * int main( int argc, char const *argv[] ) 
 * 
 * Summary of the main function:
 * 
 *    Receives per parameter the type of matrix to generate, its size and the
 *    type of multiplication to perform.
 * 
 * Parameters   : 
 *    argc
 *    argv
 * 
 * Return Value : 
 *   -1 (EXIT_FAILURE): if something goes wrong.
 *    0 (EXIT_SUCESS) : if the multiplication ends correctly.
 * 
 * Description: 
 * 
 *    This function utilizes the standard bubble sort algorithm... 
 *    Note, the array is modified in place. 
 * 
 * Usage:
 *    ./main [MATRIX_TYPE] [MATRIX_SIZE] [MULTIPLICATION_TYPE]
 * 
 *      [MATRIX_TYPE] = {RAND, SEQ}
 *      [MULTIPLICATION_TYPE] = {MULTITHREAD, NORMAL, TRANSPOSE}
 */
int main(int argc, char const *argv[])
{
    // Intializes random number generator
    srand((unsigned)time(NULL));

    // Reads the params passed by the user
    if (argc < 4)
    {
        fprintf(stderr, "[ERROR] Wrong parameters.\nUsage: ./main "
                        "[MATRIX_TYPE] [MATRIX_SIZE] [MULTIPLICATION_TYPE]\n");
        return EXIT_FAILURE;
    }

    char *type;
    enum MATRIX_TYPE Mat_type;
    enum MULTIPLICATION_TYPE Mul_type;

    // The first parameter is checked for correctness
    type = (char *)argv[1];

    if (strcmp(type, "RAND") == 0)
    {
        Mat_type = RAND;
    }
    else if (strcmp(type, "SEQ") == 0)
    {
        Mat_type = SEQ;
    }
    else
    {
        fprintf(stderr, "[ERROR] Wrong matrix type: %s.\n", type);
        return EXIT_FAILURE;
    }

    // We will use square matrixes
    const unsigned dim_x_and_y = atol(argv[2]);
    if (dim_x_and_y < 0 || dim_x_and_y > MAX_MATRIX_SIZE)
    {
        fprintf(stderr, "[ERROR] Matrix size out of bounds [0-%d].\n",
                MAX_MATRIX_SIZE);
        return EXIT_FAILURE;
    }
    const unsigned rows_a = dim_x_and_y;
    const unsigned cols_a = dim_x_and_y;
    const unsigned rows_b = dim_x_and_y;
    const unsigned cols_b = dim_x_and_y;

    // Check the type of multiplication
    type = (char *)argv[3];
    if (strcmp(type, "MULTITHREAD") == 0)
    {
        Mul_type = MULTITHREAD;
    }
    else if (strcmp(type, "NORMAL") == 0)
    {
        Mul_type = NORMAL;
    }
    else if (strcmp(type, "TRANSPOSE") == 0)
    {
        Mul_type = TRANSPOSE;
    }
    else
    {
        fprintf(stderr, "[ERROR] Wrong multiplication type: %s.\n", type);
        return EXIT_FAILURE;
    }

    // Reserve memory
    double *M_a = (double *)malloc(rows_a * cols_a * sizeof(double));
    double *M_b = (double *)malloc(rows_b * cols_b * sizeof(double));
    double *M_c = NULL;
    if (!M_a || !M_b)
    {
        fprintf(stderr, "[ERROR] Couldn't allocate memory.\n");
        exit(EXIT_FAILURE);
    }

    // Populate the matrixes
    switch (Mat_type)
    {
    case RAND:
        init_rand(M_a, rows_a, cols_a);
        init_rand(M_b, rows_b, cols_b);
        break;
    case SEQ:
        init_seq(M_a, rows_a, cols_a);
        init_seq(M_b, rows_b, cols_b);
        break;
    default:
        break; // This line should never be executed
    }

#ifdef MY_PAPI
    // ? Define values
    int eventSet = my_start_events(events, num_events);
    long long *values = (long long *)my_malloc(num_events * sizeof(long long));
    int num_cpus = 8;
    int *m_eventSets;
    const int cpus[] = {0, 1, 2, 3, 4, 5, 6, 7};
    my_attach_all_cpus_start();
#endif // MY_PAPI

    // ROI -> Matrices are multiplied
    switch (Mul_type)
    {
    case MULTITHREAD:
#ifdef MY_PAPI
        // The measure is multithread, so we need to stop the regular measure
        my_stop_events(eventSet, num_events, NULL);
        m_eventSets = my_attach_and_start(num_cpus, cpus, events, num_events);
#endif // MY_PAPI
        M_c = mat_mul_multithread(M_a, rows_a, cols_a, M_b, rows_b, cols_b);
        break;
    case NORMAL:
        M_c = mat_mul(M_a, rows_a, cols_a, M_b, rows_b, cols_b);
        break;
    case TRANSPOSE:
        M_c = mat_mul_transpose(M_a, rows_a, cols_a, M_b, rows_b, cols_b);
        break;
    default:
        break; // This line should never be executed
    }

#ifdef MY_PAPI
    if (Mul_type == MULTITHREAD)
    {
        long long **m_values;
        m_values = my_attach_and_stop(num_cpus, m_eventSets, num_events);
        my_print_attached_values(num_events, events, m_values, num_cpus, cpus);
        my_free(m_eventSets);
        my_free(m_values);
    }
    else
    {
        my_stop_events(eventSet, num_events, values);
#ifndef RAW
        my_print_values(num_events, events, values);
#else
        my_print_values_perf(num_events, events, values);
#endif
    }
    my_free(values);
#endif // MY_PAPI

#ifdef DEBUG
    printf("Matrix A: %s\n", arr_to_str(M_a, rows_a, cols_a));
    printf("Matrix B: %s\n", arr_to_str(M_b, rows_b, cols_b));
    printf("Matrix C: %s\n", arr_to_str(M_c, rows_a, cols_b));
#endif // DEBUG

    // Free memory
    mat_free(M_a);
    mat_free(M_b);
    mat_free(M_c);

    return EXIT_SUCCESS;
}
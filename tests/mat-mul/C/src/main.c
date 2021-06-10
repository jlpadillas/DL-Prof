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

#define MAX_MATRIX_SIZE 100000

#ifdef MY_PAPI
// ! NOTE: num. max. of events is 6. More and PAPI will throw an error
// TODO: Modify this lines:
// char *file = "../../../my_papi/conf/events_pc.cfg";
char *file = "../../../my_papi/conf/events_node_matmul.cfg";
// char *file = "../../../my_papi/conf/events_laptop.cfg";
// char *csv_file = "out/C_mat-mul.csv";
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

    // We will use square matrices
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

    // Populate the matrices
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
    // Set the common variables for my_PAPI execution
    // int *cpus = NULL;
    // int num_cpus = 1;
    int num_cpus = 30;
    int cpus_list[num_cpus];
    for(int i = 2; i < 32; i++)
    {
        cpus_list[i-2] = i;
    }
    int *cpus = cpus_list;
    // // If the measure is multihread, we have to modify the values
    // if (Mul_type == MULTITHREAD)
    // {
    //     num_cpus = my_get_total_cpus();
    // }

    // ! Start measure
    my_prepare_measure(file, num_cpus, cpus);
    my_start_measure();
#endif // MY_PAPI

    /* ------------------------- Region of Interest ------------------------ */
    // Matrices are multiplied
    switch (Mul_type)
    {
    case MULTITHREAD:
        M_c = mat_mul_multithread(M_a, rows_a, cols_a, M_b, rows_b, cols_b);
        break;
    case NORMAL:
        M_c = mat_mul(M_a, rows_a, cols_a, M_b, rows_b, cols_b);
        break;
    case TRANSPOSE:
        M_c = mat_mul_transpose(M_a, rows_a, cols_a, M_b, rows_b, cols_b);
        break;
    default:
        // Never should execute this option
        break;
    }
    /* ----------------------- END Region of Interest ---------------------- */

#ifdef MY_PAPI
    // ! End measure
    my_stop_measure();
    char *csv_file = NULL;
    if (argc == 5)
    {
        // The user want to print the measure in a csv_file
        csv_file = (char *)argv[4];
    }
    my_print_measure(csv_file);
    my_finalize_measure();
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
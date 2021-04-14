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

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "matrix.h"

// #define DEBUG
#define MAX_MATRIX_SIZE 100000

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

    // ROI -> Matrices are multiplied
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
        break; // This line should never be executed
    }

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
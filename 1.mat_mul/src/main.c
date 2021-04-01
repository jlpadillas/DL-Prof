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
#include <time.h>
#include "matrix.h"

#define DEBUG
/** 
 * int main( int argc, char const *argv[] ) 
 * 
 * Summary of the main function:
 * 
 *    The Sort function, rearranges the given array of 
 *    integers from highest to lowest 
 * 
 * Parameters   : array: containing integers 
 * 
 * Return Value : Nothing -- Note: Modifies the array "in place". 
 * 
 * Description: 
 * 
 *    This function utilizes the standard bubble sort algorithm... 
 *    Note, the array is modified in place. 
 * 
 * Usage:
 *    ./main [MATRIX_TYPE] [MATRIX_SIZE] [MULTIPLICATION_TYPE]
 *
 */
int main(int argc, char const *argv[])
{
    // Intializes random number generator
    srand((unsigned)time(NULL));

    // Reads the params passed by the user
    // if (argc < 4)
    // {
    //     fprintf(stderr, "[ERROR] Wrong parameters!\nUsage: ./main "
    //                     "[MATRIX_TYPE] [MATRIX_SIZE] [MULTIPLICATION_TYPE]\n");
    //     return EXIT_FAILURE;
    // }

    // We will use square matrixes
    // const unsigned dim_x_and_y = atol(argv[2]);
    const unsigned dim_x_and_y = 5;
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
        fprintf(stderr, "[ERROR] Couldn't allocate memory.\n");
        exit(EXIT_FAILURE);
    }

    // Populate the matrixes
    // init_rand(M_a, rows_a, cols_a);
    // init_rand(M_b, rows_b, cols_b);
    init_seq(M_a, rows_a, cols_a);
    init_seq(M_b, rows_b, cols_b);

    // ROI -> Matrices are multiplied
    M_c = mat_mul_transpose(M_a, rows_a, cols_a, M_b, rows_b, cols_b);

#ifdef DEBUG
    printf("Matrix A: %s\n", arr_to_str(M_a, rows_a, cols_a));
    printf("Matrix B: %s\n", arr_to_str(M_b, rows_b, cols_b));
    printf("Matrix C: %s\n", arr_to_str(M_c, rows_a, cols_b));
#endif // DEBUG

    // Free memory
    free(M_a);
    free(M_b);
    free(M_c);

    return EXIT_SUCCESS;
}
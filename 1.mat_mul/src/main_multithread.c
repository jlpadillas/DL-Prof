#include <stdlib.h>
#include <stdio.h>
#include <time.h>
// #include "../../1.mat_mul/src/matrix.h"
#include "matrix.h"

int main(int argc, char const *argv[])
{
    /* Intializes random number generator */
    srand((unsigned)time(NULL));

    const unsigned dim_x_and_y = 1000;
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

    // ROI -> Se multiplican
    M_c = mat_mul_multithread(M_a, rows_a, cols_a, M_b, rows_b, cols_b);

    // printf("Matrix A: %s\n", arr_to_str(M_a, rows_a, cols_a));
    // printf("Matrix B: %s\n", arr_to_str(M_b, rows_b, cols_b));
    // printf("Matrix C: %s\n", arr_to_str(M_c, rows_a, cols_b));

    free(M_a);
    free(M_b);
    free(M_c);

    return EXIT_SUCCESS;
}

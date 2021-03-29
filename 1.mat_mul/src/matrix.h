#ifndef MATRIX_H
#define MATRIX_H

// Maximum value of a single element of the arrays
#define MAX_RANDOM 10
// Number of threads
#define NUM_THREADS 4

void *__multi(void *arg);

/*************************************************************************
 * *arr_to_str
 *  Description:
 *      This method returns a pointer to the string with the matrix.
 *  Parameters:
 *      input   M      - Pointer to the matrix M.
 *      input   rows   - Number of rows in the matrix.
 *      input   cols   - Number of columns in the matrix.
 *  Returns:
 *      Pointer to a string.
 ************************************************************************/
char *arr_to_str(const double *M, const unsigned rows, const unsigned cols);

/*************************************************************************
 * init_rand
 *  Description:
 *      This method initializes the Matrix randomly.
 *  Parameters:
 *      in/out  M     - Pointer to the matrix M which will be modified.
 *      input   rows   - Number of rows to generate.
 *      input   cols   - Number of columns to generate.
 *  Returns:
 *      Nothing.
 ************************************************************************/
void init_rand(double *M, const unsigned rows, const unsigned cols);

/*************************************************************************
 * init_seq
 *  Description:
 *      This method initializes the Matrix sequentially with indices.
 *  Parameters:
 *      in/out  M      - Pointer to the matrix M which will be modified.
 *      input   rows   - Number of rows to generate.
 *      input   cols   - Number of columns to generate.
 *  Returns:
 *      Nothing.
 ************************************************************************/
void init_seq(double *M, const unsigned rows, const unsigned cols);

/*************************************************************************
 * mat_mul
 *  Description:
 *      This method multiplies two matrixes.
 *  Parameters:
 *      input   M_a      - Pointer to the matrix M_a.
 *      input   rows_a   - Number of rows in the matrix M_a.
 *      input   cols_a   - Number of columns in the matrix M_a.
 *      input   M_b      - Pointer to the matrix M_b.
 *      input   rows_b   - Number of rows in the matrix M_b.
 *      input   cols_b   - Number of columns in the matrix M_b.
 *  Returns:
 *      Pointer to the new matrix, product of the two inputs.
 ************************************************************************/
double *mat_mul(const double *M_a,
                const unsigned rows_a, const unsigned cols_a,
                const double *M_b,
                const unsigned rows_b, const unsigned cols_b);

/*************************************************************************
 * mat_mul_multithread
 *  Description:
 *      This method multiplies two matrixes using multiples threads.
 *  Parameters:
 *      input   M_a      - Pointer to the matrix M_a.
 *      input   rows_a   - Number of rows in the matrix M_a.
 *      input   cols_a   - Number of columns in the matrix M_a.
 *      input   M_b      - Pointer to the matrix M_b.
 *      input   rows_b   - Number of rows in the matrix M_b.
 *      input   cols_b   - Number of columns in the matrix M_b.
 *      input   n_trhds  - Number of threads to operate with.
 *  Returns:
 *      Pointer to the new matrix, product of the two inputs.
 ************************************************************************/
double *mat_mul_multithread(const double *M_a,
                            const unsigned rows_a, const unsigned cols_a,
                            const double *M_b,
                            const unsigned rows_b, const unsigned cols_b);

/*************************************************************************
 * mat_mul_transpose
 *  Description:
 *      This method multiplies two matrixes using the transpose with one
 *      of them.
 *  Parameters:
 *      input   M_a      - Pointer to the matrix M_a.
 *      input   rows_a   - Number of rows in the matrix M_a.
 *      input   cols_a   - Number of columns in the matrix M_a.
 *      input   M_b      - Pointer to the matrix M_b.
 *      input   rows_b   - Number of rows in the matrix M_b.
 *      input   cols_b   - Number of columns in the matrix M_b.
 *  Returns:
 *      Pointer to the new matrix, product of the two inputs.
 ************************************************************************/
double *mat_mul_transpose(const double *M_a,
                          const unsigned rows_a, const unsigned cols_a,
                          const double *M_b,
                          const unsigned rows_b, const unsigned cols_b);

#endif
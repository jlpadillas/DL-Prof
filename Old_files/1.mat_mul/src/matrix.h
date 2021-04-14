#ifndef MATRIX_H
#define MATRIX_H

#define MAX_RANDOM 10 // Maximum value of a single element of the arrays
#define NUM_THREADS 8 // Number of threads

typedef struct __mat_mul_arg
{
    int id;                // Thread id
    double *M_c;           // Matrix C
    unsigned rows_c_start; // Number of rows in matrix C
    unsigned rows_c_end;   // Number of rows in matrix C
    unsigned cols_c_start; // Number of cols in matrix C
    unsigned cols_c_end;   // Number of cols in matrix C
} MAT_MUL_ARG;

typedef struct __mat_mul
{
    double *M_a;     // Matrix A
    unsigned rows_a; // Number of rows in matrix A
    unsigned cols_a; // Number of cols in matrix A
    double *M_b;     // Matrix B
    unsigned rows_b; // Number of rows in matrix B
    unsigned cols_b; // Number of cols in matrix B
} MAT_MUL;

/*************************************************************************
 * arr_to_str
 *  Description:
 *      This method returns a pointer to the string with the matrix.
 *  Parameters:
 *      input   M      - Pointer to the matrix M.
 *      input   rows   - Number of rows in the matrix.
 *      input   cols   - Number of columns in the matrix.
 *  Returns:
 *      Pointer to a string.
 ************************************************************************/
char *arr_to_str(const double *M,
                 const unsigned rows, const unsigned cols);

/*************************************************************************
 * init_rand
 *  Description:
 *      This method initializes the Matrix randomly.
 *  Parameters:
 *      in/out  M      - Pointer to the matrix M which will be modified.
 *      input   rows   - Number of rows to generate.
 *      input   cols   - Number of columns to generate.
 *  Returns:
 *      Nothing.
 ************************************************************************/
void init_rand(double *M, const unsigned rows, const unsigned cols);

/*************************************************************************
 * init_seq
 *  Description:
 *      This method initializes the Matrix sequentially with indexes.
 *  Parameters:
 *      in/out  M      - Pointer to the matrix M which will be modified.
 *      input   rows   - Number of rows to generate.
 *      input   cols   - Number of columns to generate.
 *  Returns:
 *      Nothing.
 ************************************************************************/
void init_seq(double *M, const unsigned rows, const unsigned cols);

/*************************************************************************
 * mat_free
 *  Description:
 *      Removes the matrix and frees up memory.
 *  Parameters:
 *      input   M      - Pointer to the matrix M.
 *  Returns:
 *      Nothing.
 ************************************************************************/
void mat_free(double *M);

/*************************************************************************
 * mat_mul
 *  Description:
 *      This method multiplies two matrices.
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
 *      This method multiplies two matrices using multiples threads.
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
 *      This method multiplies two matrices using the transpose with one
 *      of them (the second one)
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

/*************************************************************************
 * __multi
 *  Description:
 *      This method multiplies two matrices using the transpose with one
 *      of them.
 *  Parameters:
 *      input   M_a      - Pointer to the matrix M_a.
 *      input   rows_a   - Number of rows in the matrix M_a.
 *      input   cols_a   - Number of columns in the matrix M_a.
 *  Returns:
 *      Pointer to the new matrix, product of the two inputs.
 ************************************************************************/
void *__multi(void *arg);

#endif
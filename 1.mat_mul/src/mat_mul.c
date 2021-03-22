#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

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
void init_seq(double *M, const unsigned rows, const unsigned cols)
{
    size_t i, j;
    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < cols; j++)
        {
            M[i * cols + j] = i * cols + j;
        }
    }
}

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
void init_rand(double *M, const unsigned rows, const unsigned cols)
{
    size_t i, j;
    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < cols; j++)
        {
            M[i * cols + j] = rand() / (double)RAND_MAX;
        }
    }
}

/*************************************************************************
 * mat_mul_slow
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
double *mat_mul_slow(const double *M_a,
                     const unsigned rows_a, const unsigned cols_a,
                     const double *M_b,
                     const unsigned rows_b, const unsigned cols_b)
{
    size_t i, j, k;

    if (cols_a != rows_b)
    {
        fprintf(stderr, "#columns A must be equal to #rows B!\n");
        exit(EXIT_FAILURE);
    }

    double *M_c = (double *)malloc(rows_a * cols_b * sizeof(double));
    if (M_c == NULL)
    {
        fprintf(stderr, "Couldn't allocate memory!\n");
        exit(EXIT_FAILURE);
    }

    for (i = 0; i < rows_a; i++)
    {
        for (k = 0; k < cols_b; k++)
        {
            double sum = 0.0;
            for (j = 0; j < cols_a; j++)
            {
                sum += M_a[i * cols_a + j] * M_b[j * cols_b + k];
            }
            M_c[i * cols_b + k] = sum;
        }
    }

    return M_c;
}

/*************************************************************************
 * print
 *  Description:
 *      This method prints the matrix.
 *  Parameters:
 *      input   M      - Pointer to the matrix M.
 *      input   rows   - Number of rows in the matrix.
 *      input   cols   - Number of columns in the matrix.
 *  Returns:
 *      Nothing.
 ************************************************************************/
void print(const double *M, const unsigned rows, const unsigned cols)
{
    size_t i, j;
    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < cols; j++)
        {
            printf("%8.3f ", M[i * cols + j]);
        }
        printf("\n");
    }
    printf("\n");
}

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
char *arr_to_str(const double *M, int length)
{
    // numero maximo de cifras = 18
    int max_digit_in_num = 18;
    char *str, *aux;
    str = (char *)malloc(max_digit_in_num * sizeof(char) * length);
    aux = (char *)malloc(max_digit_in_num * sizeof(char));
    strcpy(str, "[");
    for (int i = 0; i < length; i++)
    {
        sprintf(aux, "%.3f", M[i]);
        if (i < length - 1)
        {
            strcat(aux, ", ");
        }
        strcat(str, aux);
    }
    strcat(str, "]");
    free(aux);
    return str;
}

int main(int argc, char const *argv[])
{
    /* Intializes random number generator */
    time_t t;
    srand((unsigned)time(&t));
    srand(0);

    const unsigned scale = 1;
    const unsigned rows_a = 2 * scale;
    const unsigned cols_a = 2 * scale;
    const unsigned rows_b = 2 * scale;
    const unsigned cols_b = 2 * scale;

    double *M_a = (double *)malloc(rows_a * cols_a * sizeof(double));
    double *M_b = (double *)malloc(rows_b * cols_b * sizeof(double));
    double *M_c = NULL;
    double *M_d = NULL;

    if (!M_a || !M_b)
    {
        fprintf(stderr, "Couldn't allocate memory!\n");
        exit(EXIT_FAILURE);
    }

    init_rand(M_a, rows_a, cols_a);
    init_rand(M_b, rows_b, cols_b);

    // init_seq(a, n_rows_a, n_cols_a);
    // init_seq(b, n_rows_b, n_cols_b);

    M_c = mat_mul_slow(M_a, rows_a, cols_a, M_b, rows_b, cols_b);

    // ------------------------------ ROI a medir ----------------------------- //

    // if (scale == 1)
    // {
    //     printf("Matrix A:\n");
    //     print(a, n_rows_a, n_cols_a);
    //     printf("Matrix B:\n");
    //     print(b, n_rows_b, n_cols_b);
    //     printf("Matrix C:\n");
    //     print(c, n_rows_a, n_cols_b);
    //     // printf("Matrix D:\n");
    //     // print(d, n_rows_a, n_cols_b);
    // }
    
    // print(M_a, rows_a, cols_a);
    // printf("Array A: %s\n", arr_to_str(M_a, rows_a * cols_a));
    // printf("Array B: %s\n", arr_to_str(M_b, rows_b * cols_b));
    // printf("Array C: %s\n", arr_to_str(M_c, rows_a * cols_b));

    free(M_a);
    free(M_b);
    free(M_c);
    free(M_d);

    return EXIT_SUCCESS;
}

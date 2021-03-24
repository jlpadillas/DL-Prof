#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "matrix.h"


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

void init_rand(double *M, const unsigned rows, const unsigned cols)
{
    size_t i, j;
    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < cols; j++)
        {
            M[i * cols + j] = rand() / MAX_RANDOM;
        }
    }
}

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

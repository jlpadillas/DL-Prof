#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "matrix.h"

char *arr_to_str(const double *M,
                 const unsigned rows, const unsigned cols)
{
    size_t i, j;
    char *str, *aux;
    int max_digit_in_num = 18; // 18 chars/number
    str = (char *)malloc(max_digit_in_num * sizeof(char) * rows * cols);
    aux = (char *)malloc(max_digit_in_num * sizeof(char));
    strcpy(str, "\n");
    for (i = 0; i < rows; i++)
    {
        strcat(str, "|\t");
        for (j = 0; j < cols; j++)
        {
            sprintf(aux, "%8.3f", M[i * cols + j]);
            if (j < cols - 1)
            {
                strcat(aux, "\t");
            }
            else if (j < cols)
            {
                strcat(aux, "\t|\n");
            }
            strcat(str, aux);
        }
    }
    free(aux);
    return str;
}

void init_rand(double *M, const unsigned rows, const unsigned cols)
{
    size_t i, j;
    for (i = 0; i < rows; i++)
    {
        for (j = 0; j < cols; j++)
        {
            M[i * cols + j] = (double)(rand()) /
                              ((double)RAND_MAX) * MAX_RANDOM;
        }
    }
}

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

void mat_free(double *M)
{
    free(M);
}

double *mat_mul(const double *M_a,
                const unsigned rows_a, const unsigned cols_a,
                const double *M_b,
                const unsigned rows_b, const unsigned cols_b)
{
    size_t i, j, k;
    if (cols_a != rows_b)
    {
        fprintf(stderr, "[ERROR] #columns A must be equal to #rows B.\n");
        exit(EXIT_FAILURE);
    }
    double *M_c = (double *)malloc(rows_a * cols_b * sizeof(double));
    if (M_c == NULL)
    {
        fprintf(stderr, "[ERROR] Couldn't allocate memory.\n");
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

double *mat_mul_multithread(const double *M_a,
                            const unsigned rows_a, const unsigned cols_a,
                            const double *M_b,
                            const unsigned rows_b, const unsigned cols_b)
{
    // TODO: Let's start with square matrices (nxn)
    size_t i;
    pthread_t threads[NUM_THREADS];
    if (cols_a != rows_b)
    {
        fprintf(stderr, "[ERROR] #columns A must be equal to #rows B.\n");
        exit(EXIT_FAILURE);
    }
    double *M_c = (double *)malloc(rows_a * cols_b * sizeof(double));
    if (M_c == NULL)
    {
        fprintf(stderr, "[ERROR] Couldn't allocate memory.\n");
        exit(EXIT_FAILURE);
    }
    // Creating the struct to pass with all the parameters needed
    MAT_MUL_ARG aux;
    aux.M_a = (double *)M_a;
    aux.rows_a = rows_a;
    aux.cols_a = cols_a;
    aux.M_b = (double *)M_b;
    aux.rows_b = rows_b;
    aux.cols_b = cols_b;
    aux.M_c = M_c;

    // MAT_MUL_ARG aux = {
    //     aux.M_a = (double *)M_a,
    //     aux.rows_a = rows_a,
    //     aux.cols_a = cols_a,
    //     aux.M_b = M_b,
    //     aux.rows_b = rows_b,
    //     aux.cols_b = cols_b,
    //     aux.M_c = M_c};

    // TODO: The last thread operates the rest. Modify in a future and
    // TODO: let the first thread to end, operate the rest.
    // unsigned int elements_Mc = rows_a * cols_b;
    // unsigned int elements_per_thread = elements_Mc / NUM_THREADS;
    // unsigned int rest = elements_Mc % NUM_THREADS;

    // TODO: Let's make it ez and let the thread operate all the row:
    unsigned int rows_per_thread = rows_a / NUM_THREADS;
    unsigned int rest_of_matrix = rows_a % NUM_THREADS;
    aux.cols_c_start = 0;
    aux.cols_c_end = cols_b;

    // Creating NUM_THREADS threads, each evaluating its own part
    for (i = 0; i < NUM_THREADS; i++)
    {
        aux.id = i;
        aux.rows_c_start = rows_per_thread * i;
        aux.rows_c_end = aux.rows_c_start + rows_per_thread;
        if (i == NUM_THREADS - 1 && rest_of_matrix != 0)
        {
            aux.rows_c_end += rest_of_matrix;
        }
        if ((pthread_create(&threads[i], NULL, (void *)__multi,
                            (void *)&aux)) < 0)
        {
            fprintf(stderr, "[Error] Couldn't create thread #%ld.\n", i);
            exit(EXIT_FAILURE);
        }
    }
    // Joining and waiting for all threads to complete
    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }
    return M_c;
}

void *__multi(void *arg)
{
    size_t i, j, k;
    MAT_MUL_ARG *aux = (MAT_MUL_ARG *)arg;

    for (i = aux->rows_c_start; i < aux->rows_c_end; i++)
    {
        for (k = aux->cols_c_start; k < aux->cols_c_end; k++)
        {
            double sum = 0.0;
            for (j = 0; j < aux->cols_a; j++)
            {
                sum += aux->M_a[i * aux->cols_a + j] * aux->M_b[j * aux->cols_b + k];
            }
            aux->M_c[i * aux->cols_b + k] = sum;
        }
    }
    pthread_exit(NULL);
}

double *mat_mul_transpose(const double *M_a,
                          const unsigned rows_a, const unsigned cols_a,
                          const double *M_b,
                          const unsigned rows_b, const unsigned cols_b)
{
    size_t i, j, k;
    if (cols_a != rows_b)
    {
        fprintf(stderr, "[ERROR] #columns A must be equal to #rows B.\n");
        exit(EXIT_FAILURE);
    }
    double *M_b_Tr = (double *)malloc(rows_b * cols_b * sizeof(double));
    double *M_c = (double *)malloc(rows_a * cols_b * sizeof(double));
    if (M_c == NULL || M_b_Tr == NULL)
    {
        fprintf(stderr, "[ERROR] Couldn't allocate memory.\n");
        exit(EXIT_FAILURE);
    }
    // Calculate the transpose
    for (i = 0; i < rows_b; i++)
    {
        for (j = 0; j < cols_b; j++)
        {
            M_b_Tr[j * rows_b + i] = M_b[i * cols_b + j];
        }
    }
    for (i = 0; i < rows_a; i++)
    {
        for (k = 0; k < cols_b; k++)
        {
            double sum = 0.0;
            for (j = 0; j < cols_a; j++)
            {
                sum += M_a[i * cols_a + j] * M_b_Tr[k * rows_b + j];
            }
            M_c[i * cols_b + k] = sum;
        }
    }
    free(M_b_Tr);
    return M_c;
}

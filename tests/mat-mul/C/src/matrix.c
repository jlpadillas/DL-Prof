#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "matrix.h"

MAT_MUL *mat_multiplying;

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
    pthread_attr_t attr;
    pthread_t threads[NUM_THREADS];
    MAT_MUL_ARG args[NUM_THREADS];

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

    // Creates a struct with all the data of the matrices
    mat_multiplying = (MAT_MUL *)malloc(sizeof(MAT_MUL));
    mat_multiplying->M_a = (double *)M_a;
    mat_multiplying->rows_a = rows_a;
    mat_multiplying->cols_a = cols_a;
    mat_multiplying->M_b = (double *)M_b;
    mat_multiplying->rows_b = rows_b;
    mat_multiplying->cols_b = cols_b;

    // TODO: Let's make it ez and let the threads operate all the row:
    unsigned int rows_per_thread = rows_a / NUM_THREADS;
    unsigned int rest_of_matrix = rows_a % NUM_THREADS;

    // initializes the thread attributes with default values
    pthread_attr_init(&attr);

    // Creating NUM_THREADS threads, each evaluating its own part
    for (i = 0; i < NUM_THREADS; i++)
    {
        // Creating the struct to pass with all the parameters needed
        args[i].id = i;
        args[i].M_c = M_c;
        // TODO: The last thread operates the rest. Modify in a future and
        // TODO: let the first thread to end, operate the rest.
        args[i].cols_c_start = 0;
        args[i].cols_c_end = cols_b;
        args[i].rows_c_start = rows_per_thread * i;
        args[i].rows_c_end = args[i].rows_c_start + rows_per_thread;

        if (i == NUM_THREADS - 1 && rest_of_matrix != 0)
        {
            args[i].rows_c_end += rest_of_matrix;
        }

        // printf("[PID=%d] COLS[%d - %d] ROWS[%d - %d]\n", args[i].id,
        //        args[i].cols_c_start, args[i].cols_c_end,
        //        args[i].rows_c_start, args[i].rows_c_end);

        if ((pthread_create(&threads[i], &attr, (void *)__multi,
                            (void *)&args[i])) < 0)
        {
            fprintf(stderr, "[Error] Couldn't create thread #%ld.\n", i);
            exit(EXIT_FAILURE);
        }
    }
    // Joining and waiting for all threads to complete
    for (i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }
    free(mat_multiplying);
    pthread_attr_destroy(&attr);
    return M_c;
}

void *__multi(void *arg)
{
    size_t i, j, k;
    MAT_MUL_ARG *aux = (MAT_MUL_ARG *)arg;

    double *M_a = mat_multiplying->M_a; // Matrix A
    // unsigned rows_a = mat_multiplying->rows_a; // Number of rows in matrix A
    unsigned cols_a = mat_multiplying->cols_a; // Number of cols in matrix A
    double *M_b = mat_multiplying->M_b;        // Matrix B
    // unsigned rows_b = mat_multiplying->rows_b; // Number of rows in matrix B
    unsigned cols_b = mat_multiplying->cols_b; // Number of cols in matrix B

    for (i = aux->rows_c_start; i < aux->rows_c_end; i++)
    {
        for (k = aux->cols_c_start; k < aux->cols_c_end; k++)
        {
            double sum = 0.0;
            for (j = 0; j < cols_a; j++)
            {
                sum += M_a[i * cols_a + j] * M_b[j * cols_b + k];
            }
            aux->M_c[i * cols_b + k] = sum;
        }
    }
    pthread_exit(NULL);
    free(aux);
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

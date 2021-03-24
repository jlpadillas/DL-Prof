#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "my_papi.h"
// All
#include "papi.h"
// Events:
// #include "papiStdEventDefs.h"

#define NUM_EVENTS 4

void init_seq(double *a, const unsigned n_rows_a, const unsigned n_cols_a);
void init_rand(double *a, const unsigned n_rows_a, const unsigned n_cols_a);
double *transpose(const double *m, const unsigned n_rows_m, const unsigned n_cols_m, double *t);
double *dot_simple(const double *a, const unsigned n_rows_a, const unsigned n_cols_a,
                   const double *b, const unsigned n_rows_b, const unsigned n_cols_b);
double *dot(const double *a, const unsigned n_rows_a, const unsigned n_cols_a,
            const double *b, const unsigned n_rows_b, const unsigned n_cols_b);
void print(const double *a, const unsigned n_rows_a, const unsigned n_cols_a);

int main(int argc, char const *argv[])
{
    // --------------------------------- PAPI --------------------------------- //
    /* must be initialized to PAPI_NULL before calling PAPI_create_event*/
    int EventSet = PAPI_NULL;
    /* This is where we store the values we read from the eventset */
    long long values[NUM_EVENTS];
    /* We use number to keep track of the number of events in the EventSet */
    int number = 0;
    /* Initializes the library */
    my_PAPI_library_init(PAPI_VER_CURRENT);
    /* Creating the eventset */
    my_PAPI_create_eventset(&EventSet);
    /* Add Total Instructions Executed to the EventSet */
    my_PAPI_add_event(EventSet, PAPI_TOT_INS);
    /* Add Total Cycles event to the EventSet */
    my_PAPI_add_event(EventSet, PAPI_TOT_CYC);
    /* Add Floating point events to the EventSet */
    // TODO: Cambiar si estas en portatil o sobremesa:
    // my_PAPI_add_named_event(EventSet, "SIMD_FP_256:PACKED_DOUBLE");
    // my_PAPI_add_named_event(EventSet, "FP_COMP_OPS_EXE:SSE_SCALAR_DOUBLE");

    // OR
    my_PAPI_add_named_event(EventSet, "FP_ARITH_INST_RETIRED:128B_PACKED_SINGLE");
    my_PAPI_add_named_event(EventSet, "FP_ARITH_INST_RETIRED:256B_PACKED_DOUBLE");


    /* get the number of events in the event set */
    my_PAPI_list_events(EventSet, NULL, &number);
    // --------------------------------- PAPI --------------------------------- //

    /* Intializes random number generator */
    time_t t;
    srand((unsigned)time(&t));
    srand(0);

    const unsigned scale = 200;
    // const unsigned n_rows_a = 4 * scale;
    // const unsigned n_cols_a = 3 * scale;
    // const unsigned n_rows_b = 3 * scale;
    // const unsigned n_cols_b = 2 * scale;
    const unsigned n_rows_a = 2 * scale;
    const unsigned n_cols_a = 2 * scale;
    const unsigned n_rows_b = 2 * scale;
    const unsigned n_cols_b = 2 * scale;

    double *a = malloc(n_rows_a * n_cols_a * sizeof(*a));
    double *b = malloc(n_rows_b * n_cols_b * sizeof(*b));
    double *c = NULL;
    double *d = NULL;

    if (!a || !b)
    {
        printf("Couldn't allocate memory!\n");
        exit(EXIT_FAILURE);
    }

    init_rand(a, n_rows_a, n_cols_a);
    init_rand(b, n_rows_b, n_cols_b);

    // init_seq(a, n_rows_a, n_cols_a);
    // init_seq(b, n_rows_b, n_cols_b);

    // --------------------------------- PAPI --------------------------------- //
    /* Start counting */
    my_PAPI_start(EventSet);

    // ------------------------------ ROI a medir ----------------------------- //
    c = dot_simple(a, n_rows_a, n_cols_a, b, n_rows_b, n_cols_b);

    // d = dot(a, n_rows_a, n_cols_a, b, n_rows_b, n_cols_b);
    // ------------------------------ ROI a medir ----------------------------- //

    /* Stop counting and store the values into the array */
    my_PAPI_stop(EventSet, values);
    printf("\n#######################################################\n\n");
    printf("\tTotal instructions executed are %lld \n", values[0]);
    printf("\tTotal cycles executed are %lld \n", values[1]);
    printf("\t\t> IPC:  %Lf \n", ((long double)values[0]) / ((long double)values[1]));
    printf("\tSIMD_FP_256:PACKED_DOUBLE %lld \n", values[2]);
    printf("\tFP_COMP_OPS_EXE:SSE_SCALAR_DOUBLE %lld \n", values[3]);
    printf("\n#######################################################\n");
    /* free the resources used by PAPI */
    my_PAPI_shutdown();
    // --------------------------------- PAPI --------------------------------- //

    if (scale == 1)
    {
        printf("Matrix A:\n");
        print(a, n_rows_a, n_cols_a);
        printf("Matrix B:\n");
        print(b, n_rows_b, n_cols_b);
        printf("Matrix C:\n");
        print(c, n_rows_a, n_cols_b);
        // printf("Matrix D:\n");
        // print(d, n_rows_a, n_cols_b);
    }

    free(a);
    free(b);
    free(c);
    free(d);

    return EXIT_SUCCESS;
}

// ----------------------------------------------------------------------------
// ----------------------------------------------------------------------------

#define MATMUL_1D
#ifdef MATMUL_1D

/* Matrices are represented as 1-D arrays in memory.
 * That means they are contiguous in memory.
 * Minimum dimension is 1, not 0, and internal dimensions must match. */
// @author: ivanbgd
// https://github.com/ivanbgd/Matrix-Multiplication-MatMul-C/blob/master/matmul_1d_seq.c

#include <math.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Initializes vector or matrix, sequentially, with indices. */
void init_seq(double *a, const unsigned n_rows_a, const unsigned n_cols_a)
{
    for (size_t i = 0; i < n_rows_a; i++)
    {
        for (size_t j = 0; j < n_cols_a; j++)
        {
            a[i * n_cols_a + j] = i * n_cols_a + j;
        }
    }
}

/* Initializes vector or matrix, randomly. */
void init_rand(double *a, const unsigned n_rows_a, const unsigned n_cols_a)
{
    for (size_t i = 0; i < n_rows_a; i++)
    {
        for (size_t j = 0; j < n_cols_a; j++)
        {
            a[i * n_cols_a + j] = rand() / (double)RAND_MAX;
        }
    }
}

/*  Takes and returns a new matrix, t, which is a transpose of the original one, m.
    It's also flat in memory, i.e., 1-D, but it should be looked at as a transpose
    of m, meaning, n_rows_t == n_cols_m, and n_cols_t == n_rows_m.
    The original matrix m stays intact. */
double *transpose(const double *m, const unsigned n_rows_m, const unsigned n_cols_m, double *t)
{
    for (size_t i = 0; i < n_rows_m; i++)
    {
        for (size_t j = 0; j < n_cols_m; j++)
        {
            t[j * n_rows_m + i] = m[i * n_cols_m + j];
        }
    }

    return t;
}

/* Dot product of two arrays, or matrix product
 * Allocates and returns an array.
 * This variant doesn't transpose matrix b, and it's a lot slower. */
double *dot_simple(const double *a, const unsigned n_rows_a, const unsigned n_cols_a,
                   const double *b, const unsigned n_rows_b, const unsigned n_cols_b)
{

    if (n_cols_a != n_rows_b)
    {
        printf("#columns A must be equal to #rows B!\n");
        system("pause");
        exit(-2);
    }

    double *c = malloc(n_rows_a * n_cols_b * sizeof(*c));
    if (c == NULL)
    {
        printf("Couldn't allocate memory!\n");
        system("pause");
        exit(-1);
    }

    for (size_t i = 0; i < n_rows_a; i++)
    {
        for (size_t k = 0; k < n_cols_b; k++)
        {
            double sum = 0.0;
            for (size_t j = 0; j < n_cols_a; j++)
            {
                sum += a[i * n_cols_a + j] * b[j * n_cols_b + k];
            }
            c[i * n_cols_b + k] = sum;
        }
    }

    return c;
}

/* Dot product of two arrays, or matrix product
 * Allocates and returns an array.
 * This variant transposes matrix b, and it's a lot faster. */
double *dot(const double *a, const unsigned n_rows_a, const unsigned n_cols_a,
            const double *b, const unsigned n_rows_b, const unsigned n_cols_b)
{

    if (n_cols_a != n_rows_b)
    {
        printf("#columns A must be equal to #rows B!\n");
        system("pause");
        exit(-2);
    }

    double *bt = malloc(n_rows_b * n_cols_b * sizeof(*b));

    double *c = malloc(n_rows_a * n_cols_b * sizeof(*c));

    if ((c == NULL) || (bt == NULL))
    {
        printf("Couldn't allocate memory!\n");
        system("pause");
        exit(-1);
    }

    bt = transpose(b, n_rows_b, n_cols_b, bt);

    for (size_t i = 0; i < n_rows_a; i++)
    {
        for (size_t k = 0; k < n_cols_b; k++)
        {
            double sum = 0.0;
            for (size_t j = 0; j < n_cols_a; j++)
            {
                sum += a[i * n_cols_a + j] * bt[k * n_rows_b + j];
            }
            c[i * n_cols_b + k] = sum;
        }
    }

    free(bt);

    return c;
}

/* Prints vector, or matrix. */
void print(const double *a, const unsigned n_rows_a, const unsigned n_cols_a)
{
    for (size_t i = 0; i < n_rows_a; i++)
    {
        for (size_t j = 0; j < n_cols_a; j++)
        {
            printf("%8.3f ", a[i * n_cols_a + j]);
        }
        printf("\n");
    }
    printf("\n");
}

#endif // MATMUL_1D

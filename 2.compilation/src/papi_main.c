#include "my_papi.h"
#include <stdio.h>

double mat_mul_c(double m, double n);

int main()
{
    double m = 2.5;
    double n = 5.1;
    setup();
    start_measure();
    // printf("%.2f \n", 2.1467 * 123.52143);
    printf("Result = %.2f\n", mat_mul_c(m, n));
    stop_measure();
    return 0;
}

double mat_mul_c(double m, double n)
{
    return m * n;
}
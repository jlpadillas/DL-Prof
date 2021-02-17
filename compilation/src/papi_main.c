#include "my_papi.h"
#include <stdio.h>

int main()
{
    setup();
    start_measure();
    printf("%.2f \n", 2.1467 * 123.52143);
    stop_measure();
    return 0;
}
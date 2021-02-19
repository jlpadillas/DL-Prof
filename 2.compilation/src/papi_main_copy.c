#include <stdlib.h>
#include <stdio.h>
#include "my_papi_copy.h"
// All
// #include "papi.h"
// Events:
// #include "papiStdEventDefs.h"


#define NUM_EVENTS 3

double mat_mul_c(double m, double n);

int main(int argc, char const *argv[])
{
    // --------------------------------- PAPI --------------------------------- //
    /* must be initialized to PAPI_NULL before calling PAPI_create_event*/
    int EventSet = PAPI_NULL;
    /* This is where we store the values we read from the eventset */
    long long values[NUM_EVENTS];
    /* We use number to keep track of the number of events in the EventSet */
    int number;

    /***************************************************************************
    * This part initializes the library and compares the version number of the *
    * header file, to the version of the library, if these don't match then it *
    * is likely that PAPI won't work correctly. If there is an error, retval   *
    * keeps track of the version number.                                       *
    ***************************************************************************/
    my_PAPI_library_init(PAPI_VER_CURRENT);

    /* Creating the eventset */
    my_PAPI_create_eventset(&EventSet);

    // CPI or IPC
    /* Add Total Instructions Executed to the EventSet */
    my_PAPI_add_event(EventSet, PAPI_TOT_INS);
    /* Add Total Cycles event to the EventSet */
    my_PAPI_add_event(EventSet, PAPI_TOT_CYC);

    // Floating point measures
    /* Add Floating point instructions event to the EventSet */
    my_PAPI_add_event(EventSet, PAPI_FP_OPS);

    /* Add Floating point operations event to the EventSet */

    /* get the number of events in the event set */
    number = 0;
    my_PAPI_list_events(EventSet, NULL, &number);

    // printf("There are %d events in the event set\n", number);
    // --------------------------------- PAPI --------------------------------- //

    double m = 2.5;
    double n = 5.1;

    // --------------------------------- PAPI --------------------------------- //
    /* Start counting */
    my_PAPI_start(EventSet);

    // ------------------------------ ROI a medir ----------------------------- //
    printf("Result = %.2f\n", mat_mul_c(m, n));
    // ------------------------------ ROI a medir ----------------------------- //

    /* Stop counting and store the values into the array */
    my_PAPI_stop(EventSet, values);
    printf("\n#######################################################\n\n");

    printf("\tTotal instructions executed are %lld \n", values[0]);
    printf("\tTotal cycles executed are %lld \n", values[1]);
    printf("\t\t> IPC:  %Lf \n", ((long double)values[0]) / ((long double)values[1]));

    printf("\tFloating point instructions are %lld \n", values[2]);
    // printf("\tFloating point operations are %lld \n", values[3]);

    printf("\n#######################################################\n");
    /* free the resources used by PAPI */
    my_PAPI_shutdown();
    // --------------------------------- PAPI --------------------------------- //

    return EXIT_SUCCESS;
}

double mat_mul_c(double m, double n)
{
    return m * n;
}
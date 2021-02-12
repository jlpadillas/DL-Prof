#include <stdio.h>
#include <stdlib.h>
#include "papi.h" /* This needs to be included every time you use PAPI */

#define NUM_EVENTS 4
#define ERROR_RETURN(retval)                                                    \
    {                                                                           \
        fprintf(stderr, "Error %d %s:line %d: \n", retval, __FILE__, __LINE__); \
        exit(retval);                                                           \
    }

double mat_mul_c(double m, double n);

int main(int argc, char const *argv[])
{
    // --------------------------------- PAPI --------------------------------- //
    /* must be initialized to PAPI_NULL before calling PAPI_create_event*/
    int EventSet = PAPI_NULL;
    /* This is where we store the values we read from the eventset */
    long long values[NUM_EVENTS];
    /* We use number to keep track of the number of events in the EventSet */
    int retval, number;
    // char errstring[PAPI_MAX_STR_LEN];

    /***************************************************************************
    * This part initializes the library and compares the version number of the *
    * header file, to the version of the library, if these don't match then it *
    * is likely that PAPI won't work correctly. If there is an error, retval   *
    * keeps track of the version number.                                       *
    ***************************************************************************/
    if ((retval = PAPI_library_init(PAPI_VER_CURRENT)) != PAPI_VER_CURRENT)
        ERROR_RETURN(retval);

    /* Creating the eventset */
    if ((retval = PAPI_create_eventset(&EventSet)) != PAPI_OK)
        ERROR_RETURN(retval);

    // CPI or IPC
    /* Add Total Instructions Executed to the EventSet */
    if ((retval = PAPI_add_event(EventSet, PAPI_TOT_INS)) != PAPI_OK)
        ERROR_RETURN(retval);
    /* Add Total Cycles event to the EventSet */
    if ((retval = PAPI_add_event(EventSet, PAPI_TOT_CYC)) != PAPI_OK)
        ERROR_RETURN(retval);

    // Branch accuracy
    /* Add Conditional branch instructions event to the EventSet */
    if ((retval = PAPI_add_event(EventSet, PAPI_BR_CN)) != PAPI_OK)
        ERROR_RETURN(retval);
    /* Add Conditional branch instructions mispredicted event to the EventSet */
    if ((retval = PAPI_add_event(EventSet, PAPI_BR_MSP)) != PAPI_OK)
        ERROR_RETURN(retval);

    /* get the number of events in the event set */
    number = 0;
    if ((retval = PAPI_list_events(EventSet, NULL, &number)) != PAPI_OK)
        ERROR_RETURN(retval);

    // printf("There are %d events in the event set\n", number);
    // --------------------------------- PAPI --------------------------------- //

    double m = 2.5;
    double n = 5.1;

    // --------------------------------- PAPI --------------------------------- //
    /* Start counting */
    if ((retval = PAPI_start(EventSet)) != PAPI_OK)
        ERROR_RETURN(retval);

    // ------------------------------ ROI a medir ----------------------------- //
    printf("Result = %.2f\n", mat_mul_c(m, n));
    // ------------------------------ ROI a medir ----------------------------- //

    /* Stop counting and store the values into the array */
    if ((retval = PAPI_stop(EventSet, values)) != PAPI_OK)
        ERROR_RETURN(retval);
    printf("\n#######################################################\n\n");

    printf("\tTotal instructions executed are %lld \n", values[0]);
    printf("\tTotal cycles executed are %lld \n", values[1]);
    printf("\t\t> IPC:  %Lf \n", ((long double)values[0]) / ((long double)values[1]));

    printf("\tTotal branches are %lld \n", values[2]);
    printf("\tTotal branches misspredicted are %lld \n", values[3]);
    printf("\t\t> Branch acc.:  %Lf \n", 100.0 * ((long double)values[3]) / ((long double)values[2]));

    printf("\n#######################################################\n");
    /* free the resources used by PAPI */
    PAPI_shutdown();
    // --------------------------------- PAPI --------------------------------- //

    return EXIT_SUCCESS;
}

double mat_mul_c(double m, double n)
{
    return m * n;
}
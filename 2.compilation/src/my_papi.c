#include <stdlib.h>
#include <stdio.h>
#include "papi.h"

#define NUM_EVENTS 3
#define ERROR_RETURN(retval)                                                    \
    {                                                                           \
        fprintf(stderr, "Error %d %s:line %d: \n", retval, __FILE__, __LINE__); \
        exit(retval);                                                           \
    }

/* Must be initialized to PAPI_NULL before calling PAPI_create_event*/
int EventSet = PAPI_NULL;
/* This is where we store the values we read from the eventset */
long long values[NUM_EVENTS];
/* We use number to keep track of the number of events in the EventSet */
int retval, number;

int setup()
{
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

    // Floating point measures
    /* Add Floating point instructions event to the EventSet */
    if ((retval = PAPI_add_event(EventSet, PAPI_FP_OPS)) != PAPI_OK)
        ERROR_RETURN(retval);
    /* Add Floating point operations event to the EventSet */
    // if ((retval = PAPI_add_event(EventSet, PAPI_FML_INS)) != PAPI_OK)
    //     ERROR_RETURN(retval);

    /* get the number of events in the event set */
    number = 0;
    if ((retval = PAPI_list_events(EventSet, NULL, &number)) != PAPI_OK)
        ERROR_RETURN(retval);

    // printf("There are %d events in the event set\n", number);
    return EXIT_SUCCESS;
}

int start_measure()
{
    /* Start counting */
    if ((retval = PAPI_start(EventSet)) != PAPI_OK)
        ERROR_RETURN(retval);
    return EXIT_SUCCESS;
}

int stop_measure()
{
    /* Stop counting and store the values into the array */
    if ((retval = PAPI_stop(EventSet, values)) != PAPI_OK)
        ERROR_RETURN(retval);
    printf("\n#######################################################\n\n");

    printf("\tTotal instructions executed are %lld \n", values[0]);
    printf("\tTotal cycles executed are %lld \n", values[1]);
    printf("\t\t> IPC:  %Lf \n", ((long double)values[0]) / ((long double)values[1]));

    printf("\tFloating point instructions are %lld \n", values[2]);
    printf("\tFloating point operations are %lld \n", values[3]);

    printf("\n#######################################################\n");
    /* free the resources used by PAPI */
    PAPI_shutdown();
    return EXIT_SUCCESS;
}
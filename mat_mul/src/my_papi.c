#include <stdlib.h>
#include <stdio.h>
#include "papi.h"
#include "my_papi.h"

// /* Number of the events to measure */
// int num_events;
// /* Must be initialized to PAPI_NULL before calling PAPI_create_event */
// int EventSet = PAPI_NULL;
// /* This is where we store the values we read from the eventset */
// long long *values;
/* We use retval to keep track of the number of the return value */
int retval;

// *********************************************************************** //

int my_PAPI_add_event(int EventSet, int Event)
{
    if ((retval = PAPI_add_event(EventSet, Event)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_add_named_event(int EventSet, const char *EventName)
{
    // printf("\tPAPI: '%s'\n", EventName);
    if ((retval = PAPI_add_named_event(EventSet, EventName)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_create_eventset(int *EventSet)
{
    if ((retval = PAPI_create_eventset(EventSet)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_library_init(int version)
{
    if ((retval = PAPI_library_init(version)) != PAPI_VER_CURRENT)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_list_events(int EventSet, int *Events, int *number)
{
    if ((retval = PAPI_list_events(EventSet, NULL, number)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

void my_PAPI_shutdown(void)
{
    PAPI_shutdown();
}

int my_PAPI_start(int EventSet)
{
    if ((retval = PAPI_start(EventSet)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_stop(int EventSet, long long *values)
{
    if ((retval = PAPI_stop(EventSet, values)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

// *********************************************************************** //

int my_start_events(const char *events[], int numEvents)
{
    int eventSet = PAPI_NULL;
    size_t i;
    // Se crea la libreria
    my_PAPI_library_init(PAPI_VER_CURRENT);

    // Se crea el conjunto de eventos
    my_PAPI_create_eventset(&eventSet);

    // Se anhaden los eventos
    for (i = 0; i < numEvents; i++)
    {
        // printf("\tPAPI_EVENT to add: %s\n", events[i]);
        my_PAPI_add_named_event(eventSet, events[i]);
    }

    // Comprueba que se ha anhadido el numero correcto de eventos
    // int count;
    // my_PAPI_list_events(eventSet, count, numEvents);

    my_PAPI_start(eventSet);

    return eventSet;
}

int my_stop_events(int eventSet, int numEvents, long long *values)
{
    // Tengo que hacer el malloc aqui y otra funcion donde libere los datos
    return my_PAPI_stop(eventSet, values);
}

// TODO: char* my_print_events(...)
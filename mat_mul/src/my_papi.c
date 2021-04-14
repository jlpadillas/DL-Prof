#include <locale.h>
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
    {
        fprintf(stderr, "[Error?] Could not add event: '%s'\n", EventName);
        ERROR_RETURN(retval);
    }
    return retval;
}

int my_PAPI_create_eventset(int *EventSet)
{
    if ((retval = PAPI_create_eventset(EventSet)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

/* This initializes the library and checks the version number of the
 * header file, to the version of the library, if these don't match
 * then it is likely that PAPI won't work correctly.  
 */
int my_PAPI_library_init(int version)
{
    if ((retval = PAPI_library_init(version)) != PAPI_VER_CURRENT)
    {
        PAPI_perror("PAPI_library_init");
        ERROR_RETURN(retval);
    }
    return retval;
}

int my_PAPI_list_events(int EventSet, int *Events, int *number)
{
    if ((retval = PAPI_list_events(EventSet, NULL, number)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

// inform PAPI of the existence of a new thread
int my_PAPI_register_thread(void)
{
    if ((retval = PAPI_register_thread()) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

// inform PAPI that a previously registered thread is disappearing
int my_PAPI_unregister_thread(void)
{
    if ((retval = PAPI_unregister_thread()) != PAPI_OK)
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

// initialize thread support in the PAPI library
int my_PAPI_thread_init(unsigned long (*id_fn)(void))
{
    if ((retval = PAPI_thread_init(id_fn)) != PAPI_OK)
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

void my_print_values(int numEvents, const char *events[],
                     long long *values)
{
    setlocale(LC_NUMERIC, "");
    printf("%s\n", "+---------------------------------------+-----------------+");
    printf("| %-38s| %-16s|\n", "Event", "Value");
    printf("%s\n", "+---------------------------------------+-----------------+");
    for (int i = 0; i < numEvents; i++)
    {
        printf("| %-38s| %'-16lld|\n", events[i], values[i]);
    }
    printf("%s\n", "+---------------------------------------+-----------------+");
}

void my_print_values_perf(int numEvents, const char *events[],
                         long long *values)
{
    char separator = ':';
    for (int i = 0; i < numEvents; i++)
    {
        printf("%'lld%c%c%s\n", values[i], separator, separator, events[i]);
    }
}

// char *print_time(double *array, int length)
// {
//     // numero maximo de cifras = 18
//     int max_digit_in_num = 18;
//     char *str, *aux;
//     str = (char *)malloc(max_digit_in_num * sizeof(char) * length);
//     aux = (char *)malloc(max_digit_in_num * sizeof(char));
//     strcpy(str, "[");
//     for (int i = 0; i < length; i++)
//     {
//         sprintf(aux, "%.3f", array[i]);
//         if (i < length - 1)
//         {
//             strcat(aux, ", ");
//         }
//         strcat(str, aux);
//     }
//     strcat(str, "]");
//     free(aux);
//     return str;
// }

// *********************************************************************** //

int my_PAPI_hl_region_begin(const char *region)
{
    if ((retval = PAPI_hl_region_begin(region)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_hl_read(const char *region)
{
    if ((retval = PAPI_hl_read(region)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_hl_region_end(const char *region)
{
    if ((retval = PAPI_hl_region_end(region)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}
#ifndef MY_PAPI_H
#define MY_PAPI_H
#include "papi.h"

#define ERROR_RETURN(retval)                                \
    {                                                       \
        fprintf(stderr, "[MyPapi] Error %d %s:line %d: \n", \
                retval, __FILE__, __LINE__);                \
        exit(retval);                                       \
    }

// ----------------------------------------------------------------------------
// Constants
// ----------------------------------------------------------------------------
#define MAX_CPUS 64
#define MAX_LENGTH_EVENT_NAME 150

// ----------------------------------------------------------------------------
// Low_level
// ----------------------------------------------------------------------------
// add single PAPI preset or native hardware event to an event set
int my_PAPI_add_event(int EventSet, int Event);

// add an event by name to a PAPI event set
int my_PAPI_add_named_event(int EventSet, const char *EventName);

// Assign a component index to an existing but empty EventSet
int my_PAPI_assign_eventset_component(int EventSet, int cidx);

// create a new empty PAPI event set
int my_PAPI_create_eventset(int *EventSet);

// get information about the system hardware
const PAPI_hw_info_t *my_PAPI_get_hardware_info(void);

// Get PAPI library or event set options
int my_PAPI_get_opt(int option, PAPI_option_t *ptr);

int my_PAPI_is_initialized(void);

// initialize the PAPI library
int my_PAPI_library_init(int version);

// list the events that are members of an event set
int my_PAPI_list_events(int EventSet, int *Events, int *number);

// inform PAPI of the existence of a new thread
int my_PAPI_register_thread(void);

// Set PAPI library or event set options
int my_PAPI_set_opt(int option, PAPI_option_t *ptr);

// finish using PAPI and free all related resources
void my_PAPI_shutdown(void);

// start counting hardware events in an event set
int my_PAPI_start(int EventSet);

// stop counting hardware events in an event set and return current events
int my_PAPI_stop(int EventSet, long long *values);

// initialize thread support in the PAPI library
int my_PAPI_thread_init(unsigned long (*id_fn)(void));

// inform PAPI that a previously registered thread is disappearing
int my_PAPI_unregister_thread(void);

// ----------------------------------------------------------------------------
// Propios
// ----------------------------------------------------------------------------
void my_free(void *ptr);

int my_get_total_cpus();

void *my_malloc(size_t size);

// ----------------------------------------------------------------------------
// For python
// ----------------------------------------------------------------------------
// Prepare the env. befor starting the measurement
int my_prepare_measure(char *input_file_name, int num_cpus, int *cpus,
                       int num_event_sets, int *event_sets);
// Starts the measurement
int my_start_measure(int num_event_sets, int *event_sets);
// Stop the measurement
int my_stop_measure(int num_event_sets, int *event_sets, long long **values);
// Print the results
int my_print_measure(int num_cpus, int *cpus, long long **values,
                     char *output_file_name);
// Free values of measurement
int my_free_measure(long long **values, int num_event_sets);

// Read a file and get the events from it
int __get_events_from_file(char *input_file_name, int *num_events,
                           char **events);
// ----------------------------------------------------------------------------

#endif

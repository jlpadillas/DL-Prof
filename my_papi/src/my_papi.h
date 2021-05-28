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
#define MAX_EVENTS 10
#define MAX_LENGTH_EVENT_NAME 150
//#define DEBUGGING

// ----------------------------------------------------------------------------
// Low_level
// ----------------------------------------------------------------------------
// Add single PAPI preset or native hardware event to an event set
int my_PAPI_add_event(int EventSet, int Event);

// Add an event by name to a PAPI event set
int my_PAPI_add_named_event(int EventSet, const char *EventName);

// Assign a component index to an existing but empty EventSet
int my_PAPI_assign_eventset_component(int EventSet, int cidx);

// Create a new empty PAPI event set
int my_PAPI_create_eventset(int *EventSet);

// Get information about the system hardware
const PAPI_hw_info_t *my_PAPI_get_hardware_info(void);

// Get PAPI library or event set options
int my_PAPI_get_opt(int option, PAPI_option_t *ptr);

// Return the initialized state of the PAPI library
int my_PAPI_is_initialized(void);

// Initialize the PAPI library
int my_PAPI_library_init(int version);

// List the events that are members of an event set
int my_PAPI_list_events(int EventSet, int *Events, int *number);

// Inform PAPI of the existence of a new thread
int my_PAPI_register_thread(void);

// Set PAPI library or event set options
int my_PAPI_set_opt(int option, PAPI_option_t *ptr);

// Finish using PAPI and free all related resources
void my_PAPI_shutdown(void);

// Start counting hardware events in an event set
int my_PAPI_start(int EventSet);

// Stop counting hardware events in an event set and return current events
int my_PAPI_stop(int EventSet, long long *values);

// Initialize thread support in the PAPI library
int my_PAPI_thread_init(unsigned long (*id_fn)(void));

// ----------------------------------------------------------------------------
// Propios
// ----------------------------------------------------------------------------
int my_get_total_cpus();

// ----------------------------------------------------------------------------
// For python
// ----------------------------------------------------------------------------
// Prepare the env. before starting the measurement
int my_prepare_measure(char *input_file_name, int num_cpus, int *cpus);

// Starts the measurement
int my_start_measure();

// Stop the measurement
int my_stop_measure();

// Print the results
int my_print_measure(char *output_file_name);

// Ends the execution of the program
int my_finalize_measure();

// ----------------------------------------------------------------------------
#endif

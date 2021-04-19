#ifndef MY_PAPI_H
#define MY_PAPI_H
#include "papi.h"

#define ERROR_RETURN(retval)                                \
    {                                                       \
        fprintf(stderr, "[MyPapi] Error %d %s:line %d: \n", \
                retval, __FILE__, __LINE__);                \
        exit(retval);                                       \
    }

// -----------------------------------------------------------------------
// Constants
// -----------------------------------------------------------------------
#define MAX_CPUS 8

// -----------------------------------------------------------------------
// Low_level
// -----------------------------------------------------------------------
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

// -----------------------------------------------------------------------
// High_level
// -----------------------------------------------------------------------
int my_PAPI_hl_read(const char *region);

int my_PAPI_hl_region_begin(const char *region);

int my_PAPI_hl_region_end(const char *region);

// -----------------------------------------------------------------------
// Propios
// -----------------------------------------------------------------------
void *my_malloc(size_t size);

void my_free(void *ptr);

int *my_attach_and_start(int num_cpus, const int cpus[],
                         const char *events[], int numEvents);

long long **my_attach_and_stop(int num_cpus, int *eventSets, int numEvents);

void my_print_attached_values(int numEvents, const char *events[],
                              long long **values, int num_cpus,
                              const int cpus[]);

// ! Cambiar por paso de resultado por parametro (?)
// int my_attach_and_stop(int num_cpus, int *eventSets, long long **values,
//                        int numEvents);

void my_attach_cpus(int num_cpus, const int cpus[], int **eventSets);

void my_start_events_attached_cpus(const char *events[], int numEvents,
                                   int eventSets[], int num_eventSets);

void my_stop_events_attached_cpus(int eventSets[], int num_eventSets,
                                  long long *values[], int numEvents);

void my_print_values(int numEvents, const char *events[],
                     long long *values);

void my_print_values_perf(int numEvents, const char *events[],
                          long long *values);

int my_start_events(const char *events[], int numEvents);

int my_stop_events(int eventSet, int numEvents, long long *values);

#endif

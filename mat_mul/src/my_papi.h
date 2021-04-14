#ifndef MY_PAPI_H
#define MY_PAPI_H

#define ERROR_RETURN(retval)                                \
    {                                                       \
        fprintf(stderr, "[MyPapi] Error %d %s:line %d: \n", \
                retval, __FILE__, __LINE__);                \
        exit(retval);                                       \
    }

// -----------------------------------------------------------------------
// Low_level
// -----------------------------------------------------------------------
// add single PAPI preset or native hardware event to an event set
int my_PAPI_add_event(int EventSet, int Event);

// add an event by name to a PAPI event set
int my_PAPI_add_named_event(int EventSet, const char *EventName);

// create a new empty PAPI event set
int my_PAPI_create_eventset(int *EventSet);

// initialize the PAPI library
int my_PAPI_library_init(int version);

// list the events that are members of an event set
int my_PAPI_list_events(int EventSet, int *Events, int *number);

// inform PAPI of the existence of a new thread
int my_PAPI_register_thread(void);

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
void my_print_values(int numEvents, const char *events[],
                     long long *values);

void my_print_values_perf(int numEvents, const char *events[],
                          long long *values);

int my_start_events(const char *events[], int numEvents);

int my_stop_events(int eventSet, int numEvents, long long *values);

#endif

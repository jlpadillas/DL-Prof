#ifndef MY_PAPI_H
#define MY_PAPI_H

// #define PAPI_VERSION_NUMBER(maj, min, rev, inc) (((maj) << 24) | ((min) << 16) | ((rev) << 8) | (inc))
// #define PAPI_VERSION PAPI_VERSION_NUMBER(6, 0, 0, 1)
// #define PAPI_OK 0    /**< No error */
// #define PAPI_NULL -1 /**<A nonexistent hardware event used as a placeholder */

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

// finish using PAPI and free all related resources
void my_PAPI_shutdown(void);

// start counting hardware events in an event set
int my_PAPI_start(int EventSet);

// stop counting hardware events in an event set and return current events
int my_PAPI_stop(int EventSet, long long *values);

#endif

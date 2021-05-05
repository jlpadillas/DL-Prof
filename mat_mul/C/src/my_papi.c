#include <locale.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "my_papi.h"

// We use retval to keep track of the number of the return value
int retval;
// Array of strings which corresponds to the events to be measured
static char **events;
// Number of the events
static size_t num_events;

// ----------------------------------------------------------------------------
// Low_level
// ----------------------------------------------------------------------------
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

int my_PAPI_assign_eventset_component(int EventSet, int cidx)
{
    if ((retval = PAPI_assign_eventset_component(EventSet, cidx)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_create_eventset(int *EventSet)
{
    if ((retval = PAPI_create_eventset(EventSet)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

const PAPI_hw_info_t *my_PAPI_get_hardware_info(void)
{
    const PAPI_hw_info_t *hwinfo;
    if ((hwinfo = PAPI_get_hardware_info()) == NULL)
    {
        fprintf(stderr, "[MyPapi] Error getting the HW info. %s:line %d: \n",
                __FILE__, __LINE__);
        exit(EXIT_FAILURE);
    }
    return hwinfo;
}

int my_PAPI_get_opt(int option, PAPI_option_t *ptr)
{
    return PAPI_get_opt(option, ptr);
}

int my_PAPI_is_initialized(void)
{
    return PAPI_is_initialized();
}

int my_PAPI_library_init(int version)
{
    if ((retval = my_PAPI_is_initialized()) == PAPI_NOT_INITED)
    {
        if ((retval = PAPI_library_init(version)) != PAPI_VER_CURRENT)
        {
            PAPI_perror("[MyPapi] Error initializing the PAPI library\n");
            ERROR_RETURN(retval);
        }
    }
    return retval;
}

int my_PAPI_list_events(int EventSet, int *Events, int *number)
{
    if ((retval = PAPI_list_events(EventSet, NULL, number)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_register_thread(void)
{
    if ((retval = PAPI_register_thread()) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_unregister_thread(void)
{
    if ((retval = PAPI_unregister_thread()) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_set_opt(int option, PAPI_option_t *ptr)
{
    if ((retval = PAPI_set_opt(option, ptr)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

void my_PAPI_shutdown(void)
{
    PAPI_shutdown();
}

int my_PAPI_start(int EventSet)
{
    // printf("[My_Papi] Starting event set = %d\n", EventSet);
    if ((retval = PAPI_start(EventSet)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_stop(int EventSet, long long *values)
{
    // printf("[My_Papi] Stoping event set = %d\n", EventSet);
    if ((retval = PAPI_stop(EventSet, values)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_thread_init(unsigned long (*id_fn)(void))
{
    if ((retval = PAPI_thread_init(id_fn)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

// ----------------------------------------------------------------------------
// High_level
// ----------------------------------------------------------------------------
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

// Propios
// ----------------------------------------------------------------------------
int __get_events_from_file(char *input_file_name, int *num_events,
                           char **events)
{
    int i;
    FILE *fp;
    char *line;
    char **events_local;
    size_t num_events_local;

    fp = fopen(input_file_name, "r");
    if (fp == NULL)
    {
        fprintf(stderr, "[MyPapi] Error: couldn't open file '%s'\n",
                input_file_name);
        exit(EXIT_FAILURE);
    }

    /* ------------------------ FIRST READ of file ------------------------- */
    // Read lines of a maximum size equals to MAX_LENGTH_EVENT_NAME
    num_events_local = 0;
    line = (char *)my_malloc(MAX_LENGTH_EVENT_NAME * sizeof(char *));
    while (fgets(line, MAX_LENGTH_EVENT_NAME, fp) != NULL)
    {
        num_events_local++;
    }
    /* ----------------------- END FIRST READ of file ---------------------- */

    events_local = (char **)my_malloc(sizeof(char **) * num_events_local);

    /* ------------------------ SECOND READ of file ------------------------ */
    // Extract the events from each line and store in the array
    i = 0;
    rewind(fp);
    while (fgets(line, MAX_LENGTH_EVENT_NAME, fp) != NULL)
    {
        events_local[i] = (char *)my_malloc(sizeof(char *) * MAX_LENGTH_EVENT_NAME);
        // Substitute '\n' for '\0'
        if (line[strlen(line) - 1] == '\n')
        {
            line[strlen(line) - 1] = '\0';
        }
        strncpy(events_local[i++], line, strlen(line));
        // memcpy(events_local[i++], line, strlen(line));
        // bstrcpy(events_local[i++], line, strlen(line));
    }
    my_free(line);
    fclose(fp);
    /* ---------------------- END SECOND READ of file ---------------------- */
    *num_events = num_events_local;
    for (i = 0; i < num_events_local; i++)
    {
        events[i] = strdup((const char *)events_local[i]);
        my_free(events_local[i]);
    }
    my_free(events_local);
    return EXIT_SUCCESS;
}

int my_attach_cpus(int num_cpus, const int cpus[], int *eventSets)
{
    size_t i;
    int aux;
    PAPI_option_t opts;
    // Se crea la libreria
    my_PAPI_library_init(PAPI_VER_CURRENT);
    if (num_cpus < 1)
    {
        fprintf(stderr, "[ERROR] Need at least 1 CPU\n");
        exit(EXIT_FAILURE);
    }
    aux = my_get_total_cpus(); // Gets the total num of cpus
    if (num_cpus > aux)
    {
        num_cpus = aux;
    }

    int cidx = 0;
    for (i = 0; i < num_cpus; i++)
    {
        eventSets[i] = PAPI_NULL;
        my_PAPI_create_eventset(&eventSets[i]);
        my_PAPI_assign_eventset_component(eventSets[i], cidx);

        /* Force granularity to PAPI_GRN_SYS */
        opts.granularity.eventset = eventSets[i];
        opts.granularity.granularity = PAPI_GRN_SYS;
        my_PAPI_set_opt(PAPI_GRANUL, &opts);

        // attach event set to cpu i
        opts.cpu.eventset = eventSets[i];
        // if cpus == NULL then, order by num
        if (cpus == NULL)
        {
            // The first "num_cpus" cpus to be attached
            opts.cpu.cpu_num = i;
        }
        else
        {
            opts.cpu.cpu_num = cpus[i];
        }
        my_PAPI_set_opt(PAPI_CPU_ATTACH, &opts);
    }
    return EXIT_SUCCESS;
}

void my_free(void *ptr)
{
    if (!ptr)
    {
        // ptr is null
        fprintf(stderr, "[MyPapi] Error, invalid pointer.\n");
        exit(EXIT_FAILURE);
    }
    free(ptr);
}

int my_get_total_cpus()
{
    const PAPI_hw_info_t *hwinfo;
    // Loads the library
    my_PAPI_library_init(PAPI_VER_CURRENT);
    // Load info of the HW and get the local num of cpus
    hwinfo = my_PAPI_get_hardware_info();
    return hwinfo->totalcpus;
}

void *my_malloc(size_t size)
{
    void *ptr;
    ptr = malloc(size);
    if (!ptr)
    {
        // ptr is null
        fprintf(stderr, "[MyPapi] Error, couldn't allocate memory.\n");
        exit(EXIT_FAILURE);
    }
    return ptr;
}

int my_start_events(int num_events, const char *events[], int *eventSets,
                    int num_eventSets)
{
    size_t i, j;
    for (i = 0; i < num_eventSets; i++)
    {
        // Se anhaden los eventos
        for (j = 0; j < num_events; j++)
        {
            my_PAPI_add_named_event(eventSets[i], events[j]);
        }
    }
    // Empieza las medidas
    for (i = 0; i < num_eventSets; i++)
    {
        my_PAPI_start(eventSets[i]);
    }
    return EXIT_SUCCESS;
}

int my_stop_events(int num_events, int *eventSets, int num_eventSets,
                   long long **values)
{
    if (num_eventSets < 1 || num_events < 1)
    {
        fprintf(stderr, "[MyPapi] Error passing params (my_stop_events())\n");
        return EXIT_FAILURE;
    }
    if (num_eventSets == 1)
    {
        return my_PAPI_stop(*eventSets, *values);
    }
    else
    {
        for (int i = 0; i < num_eventSets; i++)
        {
            my_PAPI_stop(eventSets[i], values[i]);
        }
    }
    return EXIT_SUCCESS;
}

int my_configure_eventSet(int *eventSet)
{
    // Se crea la libreria
    my_PAPI_library_init(PAPI_VER_CURRENT);
    *eventSet = PAPI_NULL;
    my_PAPI_create_eventset(eventSet);
    return EXIT_SUCCESS;
}
// -----------------------------------------------------------------------

void my_print_values(int num_events, const char *events[], int num_cpus,
                     const int cpus[], long long **values)
{
    int i;

    if (cpus == NULL)
    {
        // No cpus list passed
        for (i = 0; i < num_cpus; i++)
        {
            printf("[CPU = %d] ??\n", i); // get the n first cpus
            __my_print_values(num_events, events, values[i]);
        }
    }
    else
    {
        // cpus list passed
        for (i = 0; i < num_cpus; i++)
        {
            printf("[CPU = %d]\n", cpus[i]);
            __my_print_values(num_events, events, values[i]);
        }
    }
}

void __my_print_values(int num_events, const char *events[],
                       long long *values)
{
    int i;
    long long val;
    setlocale(LC_NUMERIC, "");
    printf("%s\n",
           "+-------------------------------------------+-----------------+");
    printf("| %-42s| %-16s|\n", "Event", "Value");
    printf("%s\n",
           "+===========================================+=================+");
    for (i = 0; i < num_events; i++)
    {
        val = values[i];
        // if (val != 0)
        // {
        printf("| %-42s| %'-16lld|\n", events[i], val);
        // }
    }
    printf("%s\n",
           "+-------------------------------------------+-----------------+");
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

// ----------------------------------------------------------------------------
// For python
// ----------------------------------------------------------------------------
int my_prepare_measure(char *input_file_name, int num_cpus, int *cpus,
                       int num_event_sets, int *event_sets)
{
    int i, j;
    FILE *fp;
    char *line;

    /* -------------------------- Checking PARAMS -------------------------- */
    if (num_cpus < 0 || num_cpus > MAX_CPUS)
    {
        fprintf(stderr, "[MyPapi] Error: wrong number of cpus '%d'\n",
                num_cpus);
        exit(EXIT_FAILURE);
    }

    if (num_cpus != num_event_sets)
    {
        fprintf(stderr, "[MyPapi] Error: number of cpus must be the same as "
                        "the number of eventsets (%d != %d)\n",
                num_cpus, num_event_sets);
        exit(EXIT_FAILURE);
    }

    fp = fopen(input_file_name, "r");
    if (fp == NULL)
    {
        fprintf(stderr, "[MyPapi] Error: couldn't open file '%s'\n",
                input_file_name);
        exit(EXIT_FAILURE);
    }
    /* ------------------------ END checking PARAMS ------------------------ */

    /* ------------------------ FIRST READ of file ------------------------- */
    // Read lines of a maximum size equals to MAX_LENGTH_EVENT_NAME
    num_events = 0;
    line = (char *)my_malloc(MAX_LENGTH_EVENT_NAME * sizeof(char *));
    while (fgets(line, MAX_LENGTH_EVENT_NAME, fp) != NULL)
    {
        num_events++;
    }
    /* ----------------------- END FIRST READ of file ---------------------- */

    events = (char **)my_malloc(sizeof(char **) * num_events);

    /* ------------------------ SECOND READ of file ------------------------ */
    // Extract the events from each line and store in the array
    i = 0;
    rewind(fp);
    while (fgets(line, MAX_LENGTH_EVENT_NAME, fp) != NULL)
    {
        events[i] = (char *)my_malloc(sizeof(char *) * MAX_LENGTH_EVENT_NAME);
        // Substitute '\n' for '\0'
        if (line[strlen(line) - 1] == '\n')
        {
            line[strlen(line) - 1] = '\0';
        }
        strncpy(events[i++], line, strlen(line));
    }
    my_free(line);
    fclose(fp);
    /* ---------------------- END SECOND READ of file ---------------------- */

    /* ---------------------------- CONFIG PAPI ---------------------------- */
    int cidx = 0;
    PAPI_option_t opts;
    my_PAPI_library_init(PAPI_VER_CURRENT);
    if (num_cpus == 1)
    {
        *event_sets = PAPI_NULL;
        my_PAPI_create_eventset(event_sets);
        for (j = 0; j < num_events; j++)
        {
            my_PAPI_add_named_event(*event_sets, events[j]);
        }
    }
    else
    {
        for (i = 0; i < num_cpus; i++)
        {
            event_sets[i] = PAPI_NULL;
            my_PAPI_create_eventset(&event_sets[i]);
            my_PAPI_assign_eventset_component(event_sets[i], cidx);

            /* Force granularity to PAPI_GRN_SYS */
            opts.granularity.eventset = event_sets[i];
            opts.granularity.granularity = PAPI_GRN_SYS;
            my_PAPI_set_opt(PAPI_GRANUL, &opts);

            // attach event set to cpu i
            opts.cpu.eventset = event_sets[i];
            // if cpus == NULL then, order by num
            if (cpus == NULL)
            {
                // The first "num_cpus" cpus to be attached
                opts.cpu.cpu_num = i;
            }
            else
            {
                opts.cpu.cpu_num = cpus[i];
            }
            my_PAPI_set_opt(PAPI_CPU_ATTACH, &opts);
            // Adding events
            for (j = 0; j < num_events; j++)
            {
                my_PAPI_add_named_event(event_sets[i], events[j]);
            }
        }
    }
    /* -------------------------- END CONFIG PAPI -------------------------- */
    return EXIT_SUCCESS;
}

int my_start_measure(int num_event_sets, int *event_sets)
{
    int i;
    for (i = 0; i < num_event_sets; i++)
    {
        my_PAPI_start(event_sets[i]);
    }
    return EXIT_SUCCESS;
}

int my_stop_measure(int num_event_sets, int *event_sets, long long **values)
{
    int i;

    /* -------------------------- Checking PARAMS -------------------------- */
    if (num_event_sets < 1)
    {
        fprintf(stderr, "[MyPapi] Error: wrong number of event sets\n");
        return EXIT_FAILURE;
    }
    /* ------------------------ END checking PARAMS ------------------------ */

    /* -------------------------- STOPPING measure ------------------------- */
    for (i = 0; i < num_event_sets; i++)
    {
        values[i] = (long long *)my_malloc(sizeof(long long *) * num_events);
        my_PAPI_stop(event_sets[i], values[i]);
    }
    /* ------------------------ END STOPPING measure ----------------------- */
    return EXIT_SUCCESS;
}

int my_print_measure(int num_cpus, int *cpus, long long **values,
                     char *output_file_name)
{
    int i, j;
    FILE *fp;
    long long val;
    int *cpus_local;
    bool print_cpu, print_header;
    setlocale(LC_NUMERIC, "");

    cpus_local = (int *)my_malloc(sizeof(int *) * num_cpus);

    if (cpus == NULL)
    {
        if (num_cpus > 1)
        {
            for (i = 0; i < num_cpus; i++)
            {
                cpus_local[i] = i;
            }
        }
        else
        {
            cpus_local[0] = -1;
        }
    }
    else
    {
        cpus_local = cpus;
    }

    if (output_file_name != NULL)
    {
        fp = fopen(output_file_name, "w");
        if (fp == NULL)
        {
            fprintf(stderr, "[MyPapi] Error: couldn't open file '%s'\n",
                    output_file_name);
            exit(EXIT_FAILURE);
        }
    }
    else
    {
        fp = stdout;
    }

    for (i = 0; i < num_cpus; i++)
    {
        print_cpu = false;
        print_header = false;
        for (j = 0; j < num_events; j++)
        {
            val = values[i][j];
            if (val != 0)
            {
                print_cpu = true;
                if (print_cpu && !print_header)
                {
                    print_header = true;
                    fprintf(fp, "%s\n", "+-----+------------------------------"
                                        "-------------+-----------------+");
                    fprintf(fp, "| %s | %-42s| %-16s|\n", "CPU", "Event",
                            "Value");
                    fprintf(fp, "%s\n", "+=====+=============================="
                                        "=============+=================+");
                }
                fprintf(fp, "|  %02d | %-42s| %'-16lld|\n", cpus_local[i],
                        events[j], val);
            }
        }
        if (print_cpu)
        {
            fprintf(fp, "%s\n", "+-----+--------------------------------------"
                                "-----+-----------------+");
        }
    }

    if (output_file_name != NULL)
    {
        fclose(fp);
    }
    // else
    // {
    //     fflush(fp);
    // }
    // my_free(cpus_local);
    return EXIT_SUCCESS;
}

int my_free_measure(long long **values, int num_event_sets)
{
    int i;
    // Free events
    for (i = 0; i < num_events; i++)
    {
        my_free(events[i]);
    }
    my_free(events);

    // Free values
    for (i = 0; i < num_event_sets; i++)
    {
        my_free(values[i]);
    }
    my_free(values);
    return EXIT_SUCCESS;
}
// ----------------------------------------------------------------------------
#include <locale.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "my_papi.h"

// ----------------------------------------------------------------------------
// Global parameters
// ----------------------------------------------------------------------------
// We use retval to keep track of the number of the return value
static int retval = 0;

// Array of strings which corresponds to the events to be measured
static char **events = NULL;

// Number of the events to be measured
static size_t num_events = 0;

// Array of event sets
static int event_sets[MAX_CPUS] = {0};

// Number of event sets which should be the same as the g_num_cpus
static int num_event_sets = 0;

// CPUS where we have to measure
static int g_cpus[MAX_CPUS] = {0};

// Number of cpus which should be the same as num_event_sets
static int g_num_cpus = 0;

// Matrix were the results are stored
static long long values[MAX_CPUS][MAX_EVENTS] = {0};

// ----------------------------------------------------------------------------
// Low_level functions
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
#ifdef DEBUGGING
    printf("[My_Papi] DEBUG: my_PAPI_start(EventSet = %d)\n", EventSet);
#endif
    if ((retval = PAPI_start(EventSet)) != PAPI_OK)
        ERROR_RETURN(retval);
    return retval;
}

int my_PAPI_stop(int EventSet, long long *values)
{
#ifdef DEBUGGING
    printf("[My_Papi] DEBUG: my_PAPI_stop(EventSet = %d)\n", EventSet);
#endif
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
// Propios
// ----------------------------------------------------------------------------
int my_get_total_cpus()
{
    const PAPI_hw_info_t *hwinfo;
    my_PAPI_library_init(PAPI_VER_CURRENT);
    // Load info of the HW and get the local num of cpus
    hwinfo = my_PAPI_get_hardware_info();
    return hwinfo->totalcpus;
}

// ----------------------------------------------------------------------------
// For python
// ----------------------------------------------------------------------------
int my_prepare_measure(char *input_file_name, int num_cpus, int *cpus)
{
    int i, j;
    FILE *fp;
    const int cidx = 0;
    PAPI_option_t opts;
    char line[MAX_LENGTH_EVENT_NAME];

    /* -------------------------- Checking PARAMS -------------------------- */
    if (num_cpus < 1 || num_cpus > MAX_CPUS)
    {
        fprintf(stderr, "[MyPapi] Error: wrong number of cpus '%d'\n",
                num_cpus);
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
    while (fgets(line, MAX_LENGTH_EVENT_NAME, fp) != NULL)
    {
        num_events++;
    }
    /* ----------------------- END FIRST READ of file ---------------------- */

    events = (char **)calloc(sizeof(char **), num_events);

    /* ------------------------ SECOND READ of file ------------------------ */
    // Extract the events from each line and store them in the array
    i = 0;
    rewind(fp);
    while (fgets(line, MAX_LENGTH_EVENT_NAME, fp) != NULL)
    {
        events[i] = (char *)calloc(sizeof(char *), MAX_LENGTH_EVENT_NAME);
        // Substitute '\n' or '\r' for '\0'
        line[strcspn(line, "\r\n")] = 0;
        strncpy(events[i++], line, strlen(line));
    }
    fclose(fp);
    /* ---------------------- END SECOND READ of file ---------------------- */

    /* ---------------------------- CONFIG PAPI ---------------------------- */
    my_PAPI_library_init(PAPI_VER_CURRENT);
    for (i = 0; i < num_cpus; i++)
    {
        event_sets[i] = PAPI_NULL;
        my_PAPI_create_eventset(&event_sets[i]);
        my_PAPI_assign_eventset_component(event_sets[i], cidx);

        // Force granularity to PAPI_GRN_SYS
        opts.granularity.eventset = event_sets[i];
        opts.granularity.granularity = PAPI_GRN_SYS;
        my_PAPI_set_opt(PAPI_GRANUL, &opts);

        // Attach event set to cpu i
        opts.cpu.eventset = event_sets[i];
        // If cpus == NULL then, order by num
        if (cpus == NULL)
        {
            // The first "num_cpus" cpus to be attached
            opts.cpu.cpu_num = i;
            g_cpus[i] = i;
        }
        else
        {
            opts.cpu.cpu_num = cpus[i];
            g_cpus[i] = cpus[i];
        }
        my_PAPI_set_opt(PAPI_CPU_ATTACH, &opts);
        // Adding events
        for (j = 0; j < num_events; j++)
        {
            my_PAPI_add_named_event(event_sets[i], events[j]);
        }
    }
    /* -------------------------- END CONFIG PAPI -------------------------- */

    // Storing the num of cpus
    g_num_cpus = num_cpus;
    num_event_sets = num_cpus;

#ifdef DEBUGGING
    /* ----------------------------- DEBUGGING ----------------------------- */
    printf("[MyPapi] DEBUG: my_prepare_measure(input_file_name = '%s', ",
           input_file_name);
    printf("num_cpus = '%d', cpus = [", num_cpus);
    if (cpus == NULL)
    {
        printf("NULL");
    }
    else
    {
        for (i = 0; i < num_cpus; i++)
        {
            printf("'%d'", cpus[i]);
            if (i != num_cpus - 1)
            {
                printf(", ");
            }
        }
    }
    printf("])\n");

    printf("[MyPapi] DEBUG: my_prepare_measure(): events = [");
    for (i = 0; i < num_events; i++)
    {
        printf("'%s'", events[i]);
        if (i != num_events - 1)
        {
            printf(", ");
        }
    }
    printf("], num_events = '%zu'\n", num_events);

    printf("[MyPapi] DEBUG: my_prepare_measure(): event_sets = [");
    for (i = 0; i < MAX_CPUS; i++)
    {
        printf("'%d'", event_sets[i]);
        if (i != MAX_CPUS - 1)
        {
            printf(", ");
        }
    }
    printf("]\n");
    /* --------------------------- END DEBUGGING --------------------------- */
#endif
    return EXIT_SUCCESS;
}

int my_start_measure()
{
    int i;
    /* -------------------------- Checking PARAMS -------------------------- */
    if (num_event_sets == 0)
    {
        fprintf(stderr, "[MyPapi] Error: no event set created.\n");
        exit(EXIT_FAILURE);
    }
    /* ------------------------ END checking PARAMS ------------------------ */

    for (i = 0; i < num_event_sets; i++)
    {
        my_PAPI_start(event_sets[i]);
    }
    return EXIT_SUCCESS;
}

int my_stop_measure()
{
    int i;
    /* -------------------------- Checking PARAMS -------------------------- */
    if (num_event_sets == 0)
    {
        fprintf(stderr, "[MyPapi] Error: no event set to stop.\n");
        exit(EXIT_FAILURE);
    }
    /* ------------------------ END checking PARAMS ------------------------ */

    for (i = 0; i < num_event_sets; i++)
    {
        my_PAPI_stop(event_sets[i], values[i]);
    }
    return EXIT_SUCCESS;
}

int my_print_measure(char *output_file_name)
{
    int i, j;
    FILE *fp;
    long long val;
    setlocale(LC_NUMERIC, "");
    bool print_as_csv = false;

// #ifdef DEBUGGING
//     /* ----------------------------- DEBUGGING ----------------------------- */
//     printf("[MyPapi] DEBUG: my_print_measure(output_file_name = '%s')\n",
//            output_file_name);
//     /* --------------------------- END DEBUGGING --------------------------- */
// #endif

    if (output_file_name == NULL)
    {
        fp = stdout;
    }
    else
    {
        print_as_csv = true;
        fp = fopen(output_file_name, "a+");
        if (fp == NULL)
        {
            fprintf(stderr, "[MyPapi] Error: couldn't open file '%s'\n",
                    output_file_name);
            exit(EXIT_FAILURE);
        }
    }

    if (print_as_csv)
    {
        // Separator
        char sep = ':';
        for (i = 0; i < num_event_sets; i++)
        {
            for (j = 0; j < num_events; j++)
            {
                val = values[i][j];
                // if (val != 0)
                // {
                    fprintf(fp, "%d%c%lld%c%c%s\n", g_cpus[i], sep, val, sep,
                            sep, events[j]);
                // }
            }
        }
    }
    else
    {
        bool print_cpu, print_header;
        for (i = 0; i < g_num_cpus; i++)
        {
            print_cpu = false;
            print_header = false;
            for (j = 0; j < num_events; j++)
            {
                val = values[i][j];
                // if (val != 0)
                // {
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
                    fprintf(fp, "|  %02d | %-42s| %'-16lld|\n", g_cpus[i],
                            events[j], val);
                // }
            }
            if (print_cpu)
            {
                fprintf(fp, "%s\n", "+-----+--------------------------------------"
                                    "-----+-----------------+");
            }
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
    return EXIT_SUCCESS;
}

int my_finalize_measure()
{
    // Stops the PAPI lib
    my_PAPI_shutdown();
    // ! Frees memory (?)
    for (size_t i = 0; i < num_events; i++)
    {
        free(events[i]);
    }
    return EXIT_SUCCESS;
}
// ----------------------------------------------------------------------------
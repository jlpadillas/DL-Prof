#include <locale.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "my_papi.h"

// We use retval to keep track of the number of the return value
int retval = 0;
// Array of strings which corresponds to the events to be measured
static char **events = NULL;
// Number of the events
static size_t num_events = 0;
// Matrix were the results are stored
static long long g_values[MAX_CPUS][MAX_EVENTS] = { 0 };

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
// Propios
// ----------------------------------------------------------------------------
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

// ----------------------------------------------------------------------------
// For python
// ----------------------------------------------------------------------------
int my_prepare_measure(char *input_file_name, int num_cpus, int *cpus,
                       int num_event_sets, int *event_sets)
{
    int i, j;
    FILE *fp;
    char line[MAX_LENGTH_EVENT_NAME];

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
    while (fgets(line, MAX_LENGTH_EVENT_NAME, fp) != NULL)
    {
        num_events++;
        // printf(" - Ev[%zu] = '%s'\n", num_events, line);
    }
    /* ----------------------- END FIRST READ of file ---------------------- */

    events = (char **)calloc(sizeof(char **), num_events);

    /* ------------------------ SECOND READ of file ------------------------ */
    // Extract the events from each line and store in the array
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

            // Attach event set to cpu i
            opts.cpu.eventset = event_sets[i];
            // If cpus == NULL then, order by num
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
// #ifdef DEBUGGING
//     /* ----------------------------- DEBUGGING ----------------------------- */
//     printf("[MyPapi] input_file_name = '%s'\n", input_file_name);
//     printf("[MyPapi] num_cpus = '%d'\n", num_cpus);
//     if (cpus != NULL)
//     {
//         printf("[MyPapi] cpus = [");
//         for (i = 0; i < num_cpus; i++)
//         {
//             printf("'%d'", cpus[i]);
//             if (i != num_cpus - 1)
//             {
//                 printf(", ");
//             }
//             else
//             {
//                 printf("]\n");
//             }
//         }
//     }
//     printf("[MyPapi] events = [");
//     for (i = 0; i < num_events; i++)
//     {
//         printf("'%s'", events[i]);
//         if (i != num_events - 1)
//         {
//             printf(", ");
//         }
//         else
//         {
//             printf("]\n");
//         }
//     }
//     printf("[MyPapi] num_event_sets = '%d'\n", num_event_sets);
//     printf("[MyPapi] event_sets = [");
//     for (i = 0; i < num_event_sets; i++)
//     {
//         printf("'%d'", event_sets[i]);
//         if (i != num_event_sets - 1)
//         {
//             printf(", ");
//         }
//         else
//         {
//             printf("]\n");
//         }
//     }
//     /* --------------------------- END DEBUGGING --------------------------- */
// #endif
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
        // values[i] = (long long *)my_malloc(sizeof(long long *) * num_events);
        my_PAPI_stop(event_sets[i], g_values[i]);
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
    int cpus_local[MAX_CPUS];
    setlocale(LC_NUMERIC, "");

#ifdef DEBUGGING
    /* ----------------------------- DEBUGGING ----------------------------- */
    printf("[MyPapi] Start debugging of function '%s'\n", "my_print_measure()");
    printf("[MyPapi] num_cpus = '%d'\n", num_cpus);
    if (cpus != NULL)
    {
        printf("[MyPapi] cpus = [");
        for (i = 0; i < num_cpus; i++)
        {
            printf("'%d'", cpus[i]);
            if (i != num_cpus - 1)
            {
                printf(", ");
            }
            else
            {
                printf("]\n");
            }
        }
    }
    printf("[MyPapi] output_file_name = '%s'\n", output_file_name);
    printf("[MyPapi] events = [");
    for (i = 0; i < num_events; i++)
    {
        printf("'%s'", events[i]);
        if (i != num_events - 1)
        {
            printf(", ");
        }
        else
        {
            printf("]\n");
        }
    }
    printf("[MyPapi] End debugging of function '%s'\n", "my_print_measure()");
    /* --------------------------- END DEBUGGING --------------------------- */
#endif

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
        // cpus_local = cpus
        for (i = 0; i < num_cpus; i++)
        {
            cpus_local[i] = cpus[i];
        }
    }

    if (output_file_name != NULL)
    {
        fp = fopen(output_file_name, "w+");
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

#ifdef CSV
    // Separator
    char sep = ':';
    for (i = 0; i < num_cpus; i++)
    {
        for (j = 0; j < num_events; j++)
        {
            val = g_values[i][j];
            if (val != 0)
            {
                // fprintf(fp, "%d%c%'lld%c%c%s\n", cpus_local[i], sep, val, sep,
                //         sep, events[j]);
                fprintf(fp, "%d%c%lld%c%c%s\n", cpus_local[i], sep, val, sep,
                        sep, events[j]);
            }
        }
    }
#else
    bool print_cpu, print_header;
    for (i = 0; i < num_cpus; i++)
    {
        print_cpu = false;
        print_header = false;
        for (j = 0; j < num_events; j++)
        {
            val = g_values[i][j];
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
#endif

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

int my_free_measure(long long **values, int num_event_sets)
{
    int i;
    // Events
    for (i = 0; i < num_events; i++)
    {
        my_free(events[i]);
    }
    my_free(events);

    // Values
    for (i = 0; i < num_event_sets; i++)
    {
        my_free(values[i]);
    }
    my_free(values);
    return EXIT_SUCCESS;
}
// ----------------------------------------------------------------------------
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "my_papi.h"


int main(int argc, char const *argv[])
{
    int eventsets;
    my_prepare_measure("portatil_events.cfg", 1, NULL, 1, &eventsets);
    return 0;
}

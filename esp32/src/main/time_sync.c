#include "time_sync.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

void time_sync_task_listen(void* arg) {
    unsigned int id = (unsigned int) arg;
    int core_id = esp_cpu_get_core_id();

    while(true) {
        printf("Time sync id %u listening on core %d\n", id, core_id);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}

void time_sync_task_ble(void* arg) {
    unsigned int id = (unsigned int) arg;
    int core_id = esp_cpu_get_core_id();

    while(true) {
        printf("Time sync id %u doing bluetooth stuff on core %d\n", id, core_id);
        vTaskDelay(5000 / portTICK_PERIOD_MS);
    }
}
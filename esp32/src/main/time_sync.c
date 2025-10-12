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

// static void timer_sync_help() {
//     printf("timer_sync_help() to be implemented\n");
// }

// static void timer_sync_help_alloc() {
//     const esp_console_cmd_t cmd = {
//         .command = "help",
//         .help = "Lists all available commands for time synchronization",
//         .hint = NULL,
//         .func = &sensor_help,
//     };
//     ESP_ERROR_CHECK(esp_console_cmd_register(&cmd));
// }

// void time_sync_commands_alloc() {
//     timer_sync_help_alloc();
// }
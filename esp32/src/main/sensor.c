#include "sensor.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include <stdio.h>
#include <stdbool.h>


void sensor_task_listen(void* arg) {
    unsigned int id = (unsigned int) arg;
    int core_id = esp_cpu_get_core_id();

    while(true) {
        printf("Sensor id %u listening on core %d\n", id, core_id);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}

// static void sensor_help() {
//     printf("sensor_help() to be implemented\n");
// }

// static void sensor_help_alloc() {
//     const esp_console_cmd_t cmd = {
//         .command = "help",
//         .help = "Lists all available commands for time synchronization",
//         .hint = NULL,
//         .func = &sensor_help,
//     };
//     ESP_ERROR_CHECK(esp_console_cmd_register(&cmd));
// }

// void sensor_commands_alloc() {
//     sensor_commands_help_alloc();
// }
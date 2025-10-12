/*
 * SPDX-FileCopyrightText: 2010-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

#include <stdio.h>
#include <inttypes.h>

#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_chip_info.h"
#include "esp_flash.h"
#include "esp_system.h"

#include "console.h"
#include "time_sync.h"
#include "sensor.h"
#include "macros.h"
#include "stdbool.h"

void app_main(void)
{
    printf("Hello world!\n");

    // if we need multiple duplicate tasks, we can refactor code here
    unsigned int time_sync_id = 2;
    unsigned int sensor_id = 3;
    unsigned int ble_id = 4;
    xTaskCreatePinnedToCore(&sensor_task_listen, "sensor_core0", 4096, (void*)sensor_id, TASK_PRIO_3, NULL, SENSOR_CORE);
    xTaskCreatePinnedToCore(&time_sync_task_listen, "time_sync_listen_core1", 4096, (void*)time_sync_id, TASK_PRIO_2, NULL, TIME_SYNC_CORE);
    xTaskCreatePinnedToCore(&time_sync_task_ble, "time_sync_ble_core1", 4096, (void*)ble_id, TASK_PRIO_1, NULL, TIME_SYNC_CORE);

    // console_alloc();
}

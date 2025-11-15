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
#include "pwm.h"
#include "stdbool.h"

void app_main(void)
{
    printf("Hello world!\n");
    // configure_ledc_pwm();

    // if we need multiple duplicate tasks, we can refactor code here
    unsigned int sensor_id = 3;
    unsigned int pwm_id = 4;
    xTaskCreatePinnedToCore(&sensor_task_listen, "sensor_core0", 4096, (void*)sensor_id, TASK_PRIO_3, NULL, CORE0);
    xTaskCreatePinnedToCore(&configure_ledc_pwm, "pwm0", 4096, (void*)pwm_id, TASK_PRIO_3, NULL, CORE1);
}

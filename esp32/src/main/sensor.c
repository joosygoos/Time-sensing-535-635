#include "sensor.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "esp_adc/adc_oneshot.h" // For oneshot mode
#include "esp_adc/adc_continuous.h" // For continuous mode
#include "esp_adc/adc_cali.h" // For ADC calibration
#include "esp_adc/adc_cali_scheme.h" // For ADC calibration scheme

// #include <driver/adc.h>

#include <stdio.h>
#include <stdbool.h>
#include <time.h>

void sensor_task_listen(void* arg) {
    /*
    CURRENTLY: we hard code ADC to listen on GPIO36 (ADC1_0 which is adc unit 1 and channel 0)
               we also hard code adc attenuation to 12 DB (ADC_ATTEN_DB_12) as it appears that the input voltage
               is WAY higher than reference voltage, as raw data otherwise would be always 4095 (indicates input > ref)

               V = (Vref / k) * (data / (2^12 - 1)),    our ADC is 12 bits, k = 0.25 for 12 DB attenuation, Vref is 1.1 V by design (but can vary)
    */
    // unsigned int id = (unsigned int) arg;
    // int core_id = esp_cpu_get_core_id();

    adc_oneshot_unit_handle_t adc1_handle;  // oneshot mode, technically continuous polling better, but lets use oneshot for now

    adc_oneshot_unit_init_cfg_t init_config = {
        .unit_id = ADC_UNIT_1,
    };
    ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config, &adc1_handle));

    // Configure ADC channel
    adc_oneshot_chan_cfg_t config = {
        .bitwidth = ADC_BITWIDTH_12,
        .atten = ADC_ATTEN_DB_12, // Adjust attenuation as needed
    };
    ESP_ERROR_CHECK(adc_oneshot_config_channel(adc1_handle, ADC_CHANNEL_0, &config)); // ADC1, Channel 0 (GPIO 36)

    while(true) {

        /* GET ADC INPUT VOLTAGE */
        int raw_value;
        ESP_ERROR_CHECK(adc_oneshot_read(adc1_handle, ADC_CHANNEL_0, &raw_value));

        float voltage = (1.1 / 0.25) * ((float) raw_value / (4095));

        /* GET TIME */
        struct timespec ts;
        if (clock_gettime(CLOCK_REALTIME, &ts) == -1) {
            perror("clock_gettime error occurred in sensor.c");
        }

        double seconds_since_epoch = (double)ts.tv_sec + (double)ts.tv_nsec / 1000000000.0;

        printf("Raw ADC value is %d with input voltage %f at timestamp: %.9f\n", raw_value, voltage, seconds_since_epoch);
        // printf("Sensor id %u listening on core %d\n", id, core_id);
        vTaskDelay(500 / portTICK_PERIOD_MS);
    }
}

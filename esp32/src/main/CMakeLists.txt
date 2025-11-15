# Add new includes here so that build can detect them
idf_component_register(SRCS "main.c" "console.c" "sensor.c" "time_sync.c" "pwm.c"
                       PRIV_REQUIRES spi_flash console esp_adc lwip esp_netif nvs_flash esp_wifi esp_driver_ledc
                       INCLUDE_DIRS "")

# (Not part of the boilerplate)
# This example uses an extra component for common functions such as Wi-Fi and Ethernet connection.
set(EXTRA_COMPONENT_DIRS
    $ENV{IDF_PATH}/examples/common_components/protocol_examples_common
    ../components
)

# set(INCLUDE_DIRS
#     .
#     $ENV{IDF_PATH}/examples/common_components/protocol_examples_common/include
# )
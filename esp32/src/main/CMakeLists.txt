# Add new includes here so that build can detect them
idf_component_register(SRCS "main.c" "console.c" "sensor.c" "time_sync.c"
                       PRIV_REQUIRES spi_flash console esp_adc
                       INCLUDE_DIRS "")
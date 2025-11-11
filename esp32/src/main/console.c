#include <stdbool.h>
#include <stdio.h>

#include "console.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_console.h"


// static bool console_enabled = false;
// static bool console_repl_enabled = false;

// const static esp_console_config_t console_config = ESP_CONSOLE_CONFIG_DEFAULT();
// // const static esp_console_repl_config_t console_repl = {
// //     .max_history_len = 32,
// //     .history_save_path = NULL,
// //     .task_stack_size = 4096,
// //     .task_priority = 2,
// //     .task_core_id = tskNO_AFFINITY,
// //     .prompt = ">",
// //     .max_cmdline_length = 1024,
// // };


// void console_alloc() {
//     printf("console_alloc called\n");

//     ESP_ERROR_CHECK(esp_console_init(&console_config));
//     console_enabled = true;

//     esp_console_repl_t *repl = NULL;
//     esp_console_repl_config_t repl_config = ESP_CONSOLE_REPL_CONFIG_DEFAULT();
//     /* Prompt to be printed before each line.
//      * This can be customized, made dynamic, etc.
//      */
//     // repl_config.prompt =  ">";
//     // repl_config.max_cmdline_length = 1024;

//     esp_console_dev_uart_config_t uart_config = ESP_CONSOLE_DEV_UART_CONFIG_DEFAULT();
//     // ESP_ERROR_CHECK(esp_console_new_repl_uart(&uart_config, &console_repl, &repl));
//     ESP_ERROR_CHECK(esp_console_new_repl_uart(&uart_config, &repl_config, &repl));

//     ESP_ERROR_CHECK(esp_console_register_help_command());

//     ESP_ERROR_CHECK(esp_console_start_repl(repl));
//     printf("\n"
//            "Please type the component you would like to run.\n");
//     console_repl_enabled = true;
// }

// void console_free() {
//     if(console_enabled) {
//         ESP_ERROR_CHECK(esp_console_deinit());
//     }
//     // if(console_repl_enabled && repl != NULL) {
//     //     ESP_ERROR_CHECK(esp_console_stop_repl(repl));
//     // }

// }

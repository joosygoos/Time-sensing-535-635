// ESP32 has 2 cores
#define CORE0 0
#define CORE1 1

// Console
#define MAX_CMD_LINE_LEN 50
#define MAX_CMD_LINE_ARGS 3

// Task Priorities, higher is more priority
#define TASK_PRIO_1         1
#define TASK_PRIO_2         2
#define TASK_PRIO_3         3

// NOTE: actually, i think redirecting esp32 output using &> should be faster than for esp32 to write to laptop file
// #define WRITE_FILEPATH "../../data/audio/joshua.txt"
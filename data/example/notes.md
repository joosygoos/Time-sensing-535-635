# Notes

I expect future data collection to be similar to the joshua_{audio|pwm}.txt file. To have millisecond level accuracy, we will
measure adc value every millisecond. We do not use newlines in txt file as it makes everything slower, but we must create a newline every
so often to flush printf buffer out or else watchdog timer will get us. The text files are basically consecutive [timestamp (float), adc value (float)], where timestamp is microsecond level time since Unix epoch and adc value is in millivolts. There will be an occasional new line, there should be Python code to trim out newlines, after that it is just consecutive [timestamp (float), adc value (float)].

**NOTE:** With our audio sensors, if sound is too high, adc output becomes 0. This will be awkward for us, so during python processing, whenever we see
0 as adc output, it is better to convert 0 to max possible adc value (i am not sure what this value is, **need python to find max adc value**)

## Naming Conventions
Since data collected depends on specific esp32, we should name the data of our files with our own names so we know which esp32 it came from. We should also
add "audio" or "pwm" to know which data it is for.
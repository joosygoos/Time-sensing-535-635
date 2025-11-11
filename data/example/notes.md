# Notes

I expect future data collection to be similar to the 1ms_interval_3mv_max_adc.txt file. To have millisecond level accuracy, we will
measure adc value every millisecond. Every line in the text file is [timestamp (float), adc value (float)], where timestamp is microsecond level time 
since Unix epoch and adc value is in millivolts. 

**NOTE:** With our audio sensors, if sound is too high, adc output becomes 0. This will be awkward for us, so during python processing, whenever we see
0 as adc output, it is better to convert 0 to max possible adc value (i am not sure what this value is, **need python to find max adc value**)
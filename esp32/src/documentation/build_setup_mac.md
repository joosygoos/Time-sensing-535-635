# Here are my notes for setting up for MacOS, can also apply to Windows!

Helpful link, good to follow these directions. After clicking link, scroll down and choose either Windows or Linux/MacOS: 

```
https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/index.html
```
**Note:** Can skip "Start a Project Section" since we already have hello world project here, can skip shortcuts for setup stuff like customization, path shortcuts, and environment variables if you want

## Commands in order for building and flashing project

### First, make sure you are in the directory of the project, here it is esp32/src
1. `. $HOME/esp/esp-idf/export.sh` (for MacOS)
2. idf.py set-target esp32
3. idf.py menuconfig 

**Note:** For Sparkfun ESP32 Thing, go to `Component config` --> `Hardware Settings` --> `Main XTAL Config` --> `Main XTAL frequency`, change `CONFIG_XTAL_FREQ` to 26 MHz, since that is what our boards use. If don't do this, monitor command shows garbage values

1. idf.py build
2. idf.py -p PORT flash 
3. idf.py -p PORT monitor 
4. To quit, use `Ctrl + ]`

Linux PORT: `/dev/tty` 

MacOS PORT: port starts with `/dev/cu.`, PORT is entire file path (Ex: `/dev/cu.usbserial-D30J3D38`)

Windows PORT: I'm not sure about port name, i think starts with `COM`

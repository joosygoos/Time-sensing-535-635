Needs espressif idf environment

# Useful commands

## xtensa-esp32-elf-objdump

1. view source code: `xtensa-esp32-elf-objdump -S --source-comment build/hello_world.elf > disassembly.s`
2. view only assembly: `xtensa-esp32-elf-objdump -d build/hello_world.elf > disassembly.s`
   
## xtensa-esp32-elf-readelf

1. View efl header: `xtensa-esp32-elf-readelf -h build/hello_world.elf`
2. View section headers: `xtensa-esp32-elf-readelf -S build/hello_world.elf`
2. View symbol table: `xtensa-esp32-elf-readelf -s build/hello_world.elf`

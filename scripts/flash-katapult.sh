https://github.com/EricZimmerman/VoronTools/blob/main/EBB_CAN.md

flash Katapult

cd katapult
make menuconfig
make clean
make

connect with usb (remember jumper)
enter DFU mode on board
lsusb
<!-- Bus 006 Device 008: ID 0483:df11 STMicroelectronics STM Device in DFU Mode -->

sudo dfu-util -a 0 -D ~/katapult/out/katapult.bin --dfuse-address 0x08000000:force:mass-erase:leave -d 0483:df11

connect with canbus (remove jumper)

cd ~/klipper
make menuconfig
make

sudo service klipper stop
python3 ~/katapult/scripts/flashtool.py -i can0 -q

Resetting all bootloader node IDs...
Checking for Katapult nodes...
Detected UUID: 7985b8ab631b, Application: Katapult
Query Complete


python3 ~/katapult/scripts/flashtool.py -i can0 -u 7985b8ab631b -f ~/klipper/out/klipper.bin

`
Attempting to connect to bootloader
Katapult Connected
Software Version: v0.0.1-75-g90eb71b
Protocol Version: 1.1.0
Block Size: 64 bytes
Application Start: 0x8002000
MCU type: stm32g0b1xx
Verifying canbus connection
Flashing '/home/biqu/klipper/out/klipper.bin'...

[##################################################]

Write complete: 15 pages
Verifying (block count = 467)...

[##################################################]

Verification Complete: SHA = 73D9CC0DDEE80D2C1CB94EB7BE763C744687EE4E
Flash Success
` 

python3 ~/katapult/scripts/flashtool.py -i can0 -q

Resetting all bootloader node IDs...
Checking for Katapult nodes...
Detected UUID: 7985b8ab631b, Application: Klipper
Query Complete

sudo service klipper start
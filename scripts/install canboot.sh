https://github.com/EricZimmerman/VoronTools/blob/main/EBB_CAN.md


Bus 006 Device 003: ID 0483:df11 STMicroelectronics STM Device in DFU Mode
Bus 006 Device 002: ID 0483:df11 STMicroelectronics STM Device in DFU Mode

sudo dfu-util -a 0 -D ~/katapult/out/katapult.bin --dfuse-address 0x08000000:force:mass-erase:leave -d 0483:df11



Detected UUID: 7985b8ab631b, Application: Katapult

python3 ~/katapult/scripts/flashtool.py -i can0 -u 7985b8ab631b -f ~/klipper/out/klipper.bin

Checking for Katapult nodes...
Detected UUID: 9f8faa6b3a15, Application: Katapult
Detected UUID: 7985b8ab631b, Application: Klipper

python3 ~/katapult/scripts/flashtool.py -i can0 -u 9f8faa6b3a15 -f ~/klipper/out/klipper.bin

Checking for Katapult nodes...
Detected UUID: 7985b8ab631b, Application: Klipper
Detected UUID: 9f8faa6b3a15, Application: Klipper


https://mpx.wiki/flash-m8p-and-ebb-sb-toolboard


log into pi so that we can compile on linux

git clone https://github.com/Klipper3d/klipper.git
make clean
make menuconfig

500000 can bus speed
make

ls /dev/serial/by-id/*
lsusb

<!-- /dev/serial/by-id/usb-Klipper_stm32g0b1xx_18003F000C50425539393020-if00 -->
<!-- 0483:df11 -->

enter DFU mode on board
lsusb
<!-- Bus 006 Device 008: ID 0483:df11 STMicroelectronics STM Device in DFU Mode -->

sudo service klipper stop
make flash FLASH_DEVICE=/dev/serial/by-id/usb-Klipper_stm32g0b1xx_18003F000C50425539393020-if00
or
make flash FLASH_DEVICE=0483:df11
sudo service klipper start

sudo apt install python3-can
python3 ./scripts/canbus_query.py can0

Found canbus_uuid=9f8faa6b3a15, Application: Klipper

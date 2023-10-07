https://mpx.wiki/flash-m8p-and-ebb-sb-toolboard


git clone https://github.com/Klipper3d/klipper.git
make clean
make menuconfig
make

ls /dev/serial/by-id/*
lsusb

<!-- /dev/serial/by-id/usb-Klipper_stm32g0b1xx_18003F000C50425539393020-if00 -->

enter DFU mode on board

sudo service klipper stop
make flash FLASH_DEVICE=/dev/serial/by-id/usb-Klipper_stm32g0b1xx_18003F000C50425539393020-if00
sudo service klipper start

sudo apt install python3-can
python3 ./scripts/canbus_query.py can0

Found canbus_uuid=9f8faa6b3a15, Application: Klipper

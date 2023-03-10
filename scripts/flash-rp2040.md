make menuconfig
choose rp2040
<!-- exit and save -->
make clean
make
<!-- find serial port name -->
ls /dev/serial/by-id/*
sudo service klipper stop
make flash FLASH_DEVICE=/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0
sudo service klipper start
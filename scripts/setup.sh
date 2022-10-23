https://github.com/th33xitus/kiauh



git clone https://github.com/Arksine/CanBoot
pip3 install pyserial
cd CanBoot
make menuconfig

# from voron documentation https://docs.vorondesign.com/build/software/octopus_klipper.html
sudo apt install make
cd ~/klipper
./scripts/install-octopi.sh
make clean
make menuconfig

sudo apt-get install klipper

clone dfu-util from github, build and install
# flash octopus
lsusb
make flash FLASH_DEVICE=0483:df11

ls /dev/serial/by-id

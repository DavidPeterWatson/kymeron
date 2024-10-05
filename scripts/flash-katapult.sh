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

python3 ~/katapult/scripts/flashtool.py -i can0 -u 7985b8ab631b -f ~/klipper/out/klipper.bin


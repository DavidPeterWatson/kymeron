https://www.raspberrypi.com/tutorials/plug-and-play-raspberry-pi-usb-webcam/

<!-- check disk space -->
df

sudo apt update
sudo apt full-upgrade
sudo reboot
echo "dtoverlay=dwc2,dr_mode=otg" | sudo tee -a /boot/config.txt
sudo apt install git meson libcamera-dev libjpeg-dev
git clone https://gitlab.freedesktop.org/camera/uvc-gadget.git
cd uvc-gadget
make uvc-gadget
cd build
sudo meson install
sudo ldconfig



<!-- try again -->

https://howchoo.com/g/ndy1zte2yjn/how-to-set-up-wifi-on-your-raspberry-pi-without-ethernet

https://linuxize.com/post/how-to-install-xrdp-on-raspberry-pi/

libcamera-vid -t 0 --width 1920 --height 1080 --codec h264 --inline --listen -o tcp://0.0.0.0:8888

https://www.waveshare.com/wiki/RPi_Zero_V1.3_Camera

https://github.com/raspberrypi/picamera2/blob/main/examples/mjpeg_server_2.py


sudo apt install raspberrypi-ui-mods xinit xserver-xorg
sudo apt install xrdp

https://wiki.kb-3d.com/en/home/btt/voron/u2c_v2#:~:text=Connecting%20your%20U2C,and%20start%20the%20initial%20configuration.

lsusb

Bus 003 Device 002: ID 1d50:606f OpenMoko, Inc. Geschwister Schneider CAN adapter

sudo nano /etc/network/interfaces.d/can0

allow-hotplug can0
  iface can0 can static
  bitrate 500000
  up ip link set can0 txqueuelen 1024


sudo reboot

ifconfig can0
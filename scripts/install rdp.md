hostname -I
cat /var/log/xrdp.log

---

https://tecadmin.net/how-to-install-xrdp-on-debian-10/

sudo apt update
sudo apt upgrade
sudo apt install tasksel
<!-- choose xfce -->
sudo systemctl set-default graphical.target
reboot
sudo apt install xrdp
sudo systemctl status xrdp
sudo usermod -a -G ssl-cert xrdp
sudo nano /etc/xrdp/startwm.sh 

<!-- Unset DBUS_SESSION_ADDRESS
Unset XDG_RUNTIME_DIR -->
sudo systemctl restart xrdp

sudo iwconfig

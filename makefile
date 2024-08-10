.PHONY: pi-shell

pi-shell:
	ssh biqu@192.168.20.200

install-led-effects:
	cd ~
	git clone https://github.com/julianschill/klipper-led_effect.git
	cd klipper-led_effect
	./install-led_effect.sh

install-tmc-autotune:
	wget -O - https://raw.githubusercontent.com/andrewmcgr/klipper_tmc_autotune/main/install.sh | bash

install-carriage-changer:
	cd ~
	git clone https://github.com/DavidPeterWatson/klipper-carriage-changer.git
	cd klipper-carriage-changer
	./install.sh

install-tool-changer:
	wget -O - https://raw.githubusercontent.com/viesturz/klipper-toolchanger/main/install.sh | bash

install-kymeron:
	cd ~
	git clone https://github.com/DavidPeterWatson/Kymeron.git

setup_can:
	sudo touch /etc/network/interfaces.d/can0
	echo "allow-hotplug can0" | sudo tee -a /etc/network/interfaces.d/can0
	echo "iface can0 can static" | sudo tee -a /etc/network/interfaces.d/can0
	echo " bitrate 1000000" | sudo tee -a /etc/network/interfaces.d/can0
	echo " up ifconfig $IFACE txqueuelen 1024" | sudo tee -a /etc/network/interfaces.d/can0
	echo " pre-up ip link set can0 type can bitrate 1000000" | sudo tee -a /etc/network/interfaces.d/can0
	echo " pre-up ip link set can0 txqueuelen 1024" | sudo tee -a /etc/network/interfaces.d/can0

	sudo touch /etc/systemd/network/10-can.link
	echo "[Match]" | sudo tee -a /etc/systemd/network/10-can.link
	echo "Type=can" | sudo tee -a /etc/systemd/network/10-can.link
	echo "[Link]" | sudo tee -a /etc/systemd/network/10-can.link
	echo "TransmitQueueLength=1024" | sudo tee -a /etc/systemd/network/10-can.link

	sudo touch /etc/systemd/network/25-can.network
	echo "[Match]" | sudo tee -a /etc/systemd/network/25-can.network
	echo "Name=can*" | sudo tee -a /etc/systemd/network/25-can.network
	echo "[CAN]" | sudo tee -a /etc/systemd/network/25-can.network
	echo "BitRate=1M" | sudo tee -a /etc/systemd/network/25-can.network

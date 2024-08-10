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
	clone https://github.com/DavidPeterWatson/klipper-carriage-changer.git

install-tool-changer:
	wget -O - https://raw.githubusercontent.com/viesturz/klipper-toolchanger/main/install.sh | bash

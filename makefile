.PHONY: pi-shell

pi-shell:
	ssh biqu@192.168.20.200

install-led-effects:
	cd ~
	git clone https://github.com/julianschill/klipper-led_effect.git
	cd klipper-led_effect
	./install-led_effect.sh
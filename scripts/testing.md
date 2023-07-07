

<!-- Install stress -->
sudo apt-get install stress

<!-- Find number of cores -->
lscpu

<!-- Stress test on all cores for 10 seconds -->
stress --cpu 4 --timeout 10

sudo apt install speedtest-cli

speedtest-cli --simple

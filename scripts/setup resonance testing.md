https://www.klipper3d.org/Measuring_Resonances.html

sudo apt update
sudo apt install python3-numpy python3-matplotlib libatlas-base-dev libopenblas-base
~/klippy-env/bin/pip install -v numpy




scp -r biqu@192.168.20.200:/tmp '/Users/david/Library/Mobile Documents/com~apple~CloudDocs/Documents/repos/github/kymeron/'


~/klipper/scripts/calibrate_shaper.py /tmp/resonances_x_*.csv -o /tmp/shaper_calibrate_x.png

Fitted shaper 'zv' frequency = 109.6 Hz (vibrations = 17.3%, smoothing ~= 0.018)
To avoid too much smoothing with 'zv', suggested max_accel <= 46800 mm/sec^2
Fitted shaper 'mzv' frequency = 71.2 Hz (vibrations = 1.6%, smoothing ~= 0.042)
To avoid too much smoothing with 'mzv', suggested max_accel <= 14900 mm/sec^2
Fitted shaper 'ei' frequency = 98.4 Hz (vibrations = 2.8%, smoothing ~= 0.035)
To avoid too much smoothing with 'ei', suggested max_accel <= 18000 mm/sec^2
Fitted shaper '2hump_ei' frequency = 102.4 Hz (vibrations = 0.0%, smoothing ~= 0.053)
To avoid too much smoothing with '2hump_ei', suggested max_accel <= 11700 mm/sec^2
Fitted shaper '3hump_ei' frequency = 122.4 Hz (vibrations = 0.0%, smoothing ~= 0.056)
To avoid too much smoothing with '3hump_ei', suggested max_accel <= 11000 mm/sec^2


~/klipper/scripts/calibrate_shaper.py /tmp/resonances_y_*.csv -o /tmp/shaper_calibrate_y.png

Fitted shaper 'zv' frequency = 115.4 Hz (vibrations = 16.7%, smoothing ~= 0.017)
To avoid too much smoothing with 'zv', suggested max_accel <= 51900 mm/sec^2
Fitted shaper 'mzv' frequency = 82.2 Hz (vibrations = 0.0%, smoothing ~= 0.033)
To avoid too much smoothing with 'mzv', suggested max_accel <= 19900 mm/sec^2
Fitted shaper 'ei' frequency = 100.8 Hz (vibrations = 0.3%, smoothing ~= 0.034)
To avoid too much smoothing with 'ei', suggested max_accel <= 18900 mm/sec^2
Fitted shaper '2hump_ei' frequency = 121.8 Hz (vibrations = 0.0%, smoothing ~= 0.039)
To avoid too much smoothing with '2hump_ei', suggested max_accel <= 16500 mm/sec^2
Fitted shaper '3hump_ei' frequency = 145.6 Hz (vibrations = 0.0%, smoothing ~= 0.042)
To avoid too much smoothing with '3hump_ei', suggested max_accel <= 15500 mm/sec^2
Recommended shaper is mzv @ 82.2 Hz
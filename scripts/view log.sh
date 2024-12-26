/home/biqu/printer_data/logs

mkdir work_directory
cd work_directory
cp /home/biqu/printer_data/logs/klippy.log .
~/klipper/scripts/logextract.py ./klippy.log

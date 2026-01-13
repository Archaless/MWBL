*** MAKE SURE YOU ARE CONNECTED TO INTERNET SOME WAY, I CONNECT TO A HOTSPOT ON MY PHONE WITH 'sudo nmtui' ***

1. 'cd' into wherever this USB drive is mounted
	ex. 'cd /media/USBDrive'
2. 'bash RPI_Setup_Online.sh' (type 'n' if prompted to overwrite anything)
3. 'source ~/.bashrc' (this doesn't work in the script)
4. Share rsa key with required computers
	ex. 'ssh-copy-id pi@192.168.1.1'
5. Double check cronjobs
	ex. 'crontab -e'
6. Replace/modify '/home/pi/Scripts/GetDataPi.py' and '/home/pi/Scripts/config.py'
NOTE: if pi is logging multiple sensors:
	I. Create a new folder for each 'config.py' file
	II. Update 'crontab -e' with PYTHONPATH='/home/pi/Scripts/*new sensor folder*:$PYTHONPATH' before each corresponding log_main.py cmd
		ex. PYTHONPATH="/home/pi/Scripts/MKIII/:$PYTHONPATH" /home/pi/python/bin/python /home/pi/Scripts/log_main.py
7. If using gps to set clock:
	I. 'sudo raspi-config'
		Interface Options
		Serial Port
		Disable login shell over serial → No
		Enable serial hardware port → Yes
		Reboot when prompted
	II.  run:
		sudo echo "dtoverlay=pi3-disable-bt">>/boot/config.txt
		sudo systemctl disable hciuart.service
		sudo systemctl stop hciuart.service
		sudo reboot
8. Done!

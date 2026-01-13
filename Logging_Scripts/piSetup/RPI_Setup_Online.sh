### General Setup ###
# Date and Time
sudo timedatectl set-timezone UTC
echo "Current Time:"
date
sudo apt update
sudo apt upgrade -y
# Create rsa key for ssh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -q
# Directory Creation
mkdir /home/pi/Scripts
mkdir /home/pi/Scripts/Archive
mkdir /home/pi/Data
mkdir /home/pi/python
# Copy scripts to folder
cp ./Scripts/*.py /home/pi/Scripts
### Python Library Installation ###
# Virtual Python Environment
# Install Dependencies
sudo apt install -y gpsd gpsd-clients python3-gps python3-venv python3-dev openssl libssl-dev libffi-dev libbz2-dev libreadline-dev libsqlite3-dev zlib1g-dev
# Remove original LOCAL install (if it exists)
sudo rm -f /usr/local/bin/python3
sudo rm -f /usr/local/bin/python3.*
sudo rm -rf /usr/local/lib/python3.*
# Reinstall to use system python
sudo apt install -y --reinstall python3 python3-venv python3-pip python3-setuptools python3-minimal
# Create new virtual environment based on system python
python3 -m venv /home/pi/python
# Install libraries to new install
/home/pi/python/bin/pip install pyserial
/home/pi/python/bin/pip install bs4
/home/pi/python/bin/pip install paramiko
/home/pi/python/bin/pip install requests
/home/pi/python/bin/pip install pandas
/home/pi/python/bin/pip install psutil
# Alias new Python Virtual Environment, will overwrite .bash_aliases
touch /home/pi/.bash_aliases
echo "alias pythonVEnv='/home/pi/python/bin/python'" > /home/pi/.bash_aliases
echo "alias pipVEnv='/home/pi/python/bin/pip'" >> /home/pi/.bash_aliases
# Setup Cronjob(s)
touch /home/pi/tmpcron
crontab -l > /home/pi/tmpcron
echo "@reboot sleep 20 && pythonVEnv /home/pi/Scripts/GetPiData.py" >> /home/pi/tmpcron
echo "0 0 * * * /home/pi/python/bin/python /home/pi/Scripts/GetPiData.py" >> /home/pi/tmpcron
echo "@reboot sleep 20 && /home/pi/python/bin/python /home/pi/Scripts/log_main.py" >> /home/pi/tmpcron
crontab /home/pi/tmpcron
rm /home/pi/tmpcron
# Setup gpsd
sudo mv /etc/default/gpsd /etc/default/gpsd.backup
sudo cp ./gpsd /etc/default/
sudo apt autoremove -y

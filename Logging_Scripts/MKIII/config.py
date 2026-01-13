###########################################################################
               ### Config for SMAST MKIII (PortLog) ###
###########################################################################
# Python Libraries
import os
import requests
from bs4 import BeautifulSoup
from time import time, sleep
# Local Libraries
from Serial_Scripts import connect2serial
from Network_Scripts import ping_IP
###########################################################################
                       ### Global Variables ###
###########################################################################

REQUIRED = ['device','connection','savePath'] # DO NOT REMOVE
# Misc
device = 'MKIII'
backupDays = 30 # Days
retryAttempts = 3
logTime = 'daily' # 'hourly' or 'daily'
connection = [0x1a86, 0x7523] # VID and PID (if serial), otherwise use int for eth# or -1 for wlan0
# Save Location Config:
savePath = '/home/pi/Data/MKIII/' # Local directory to upload
tmpPath = '/home/pi/Data/MKIII-tmp/' # Local directory to write data (will be moved to savePath after start of next file)
logPath = '/home/pi/' # Local directory to store log file
logFilename = 'MKIII_log.txt'
# Remote Machine Config:
hostname = '192.168.0.1' # IP Address
username = 'KZLocal' # Username
remotePath = 'C:/Users/KZLocal/Documents/MKIII/Data/' # Location to transfer saves to
# Filename Config:
titlePre = 'Rainwise_MK_W3425_'
titlePost = '_SMAST.csv'
# File Header:
header = 'time (Sec. from Epoch),air_temp (Deg. F),humidity (%)\
            ,barometric_pressure (inHg),wind speed (mph),wind direction (Deg.)\
			,precipitation (in.),solar_radiation (W/m^2)\n'

###########################################################################
                       ### Local Variables ###
###########################################################################
# Network Config Settings:
baud = 9600 # CH340 Chip (USB Relay)
vid = 0x1a86 # CH340 Chip (USB Relay)
pid = 0x7523 # CH340 Chip (USB Relay)
hostname_MKII = '192.168.0.169'
timeStep = 1 # Seconds, how often to ping site
timeout = 0.5 # Seconds, how long to wait for a response from sensor
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

###########################################################################
                           ### Functions ###
###########################################################################

def fetch(initArgs=None):
    # Send HTTP GET request
    url = 'http://' + hostname_MKII
    response = requests.get(url, headers=headers, timeout=timeStep)
    try:
        response.raise_for_status()  # Raise an error for bad status codes
    except:
        reset_Connection(baud, vid, pid)
        response = requests.get(url, headers=headers, timeout=timeStep)
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract visible text from the page
    text = soup.get_text(separator='\n', strip=True)
    varList = text.split('\n')  # Divide string into a list
    # Extract each variable (guard against parsing issues)
    try:
        air_temp = varList[17]
        humidity = varList[30]
        barometric_pressure = varList[43]
        wind = varList[56]  # speed and direction separated by a comma
        precipitation = varList[65]
        solar_radiation = varList[70]
    except Exception:
        raise IndexError(f'Unexpected HTML format, varList length: {len(varList)}')
    # Save scraped text
    data = str(time()) + ', ' + air_temp + ', ' + humidity + ', ' \
        + barometric_pressure + ', ' + wind + ', ' + precipitation \
        + ', ' + solar_radiation
    # Pause
    sleep(timeStep)
    return data

def init(logger):
    # Test connection:
    if not ping_IP(hostname_MKII) == 0:
        reset_Connection(baud, vid, pid)
        raise ValueError(f'Failed ping on: eth{connection}')
    logger.info(f'Successful ping of: {hostname_MKII}')
    return None # Whatever is returned will be passed to fetch

def cleanup(initArgs=None):  # Must have same args as init
    pass


###########################################################################
                           ### Helper Functions ###
###########################################################################

def reset_Connection(baud, vid, pid):
    waitTime = 30
    attempts = 0
    reset_Relay(baud, vid, pid)
    while not ping_IP(hostname_MKII) == 0:
        if attempts > 10: # Force exit after 10 tries
            raise ValueError(f'In config.py: reset_Relay - Timeout on: {hostname_MKII} after {attempts*waitTime} seconds')
        # Ping ip address until it responds or waitTime has passed
        sleep(waitTime)
        attempts += 1

def reset_Relay(baud, vid, pid):
    openRelay = 'A0 01 01 A2'
    closeRelay = 'A0 01 00 A1'
    with connect2serial(vid, pid, baudRate=baud) as ser:
        print('Opening!')
        ser.write(bytes.fromhex(openRelay))
        sleep(5)
        print('Closing!')
        ser.write(bytes.fromhex(closeRelay))
###########################################################################
               ### Config for SMAST MKIII (PortLog) ###
###########################################################################
# Python Libraries
import os
from urllib import response
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
retryAttempts = 10
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
timeStep = 15 # Seconds, how often to ping site
timeout = 0.5 # Seconds, how long to wait for a response from sensor
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

###########################################################################
                           ### Functions ###
###########################################################################

def fetch(initArgs=None):
    # Send HTTP GET request
    url = 'http://' + hostname_MKII

    for attempt in range(retryAttempts):
        session = requests.Session()
        try:
            response = session.get(
                url,
                headers=headers,
                timeout=(3, 5)  # (connect timeout, read timeout)
            )
            response.raise_for_status()
            break  # SUCCESS → exit retry loop
        except (requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError) as e:
            print(f"[fetch] Connection failed (attempt {attempt+1}/{retryAttempts}): {e}")
            reset_Connection(baud, vid, pid)
            # exponential backoff, capped
            sleep(30)
        except requests.exceptions.HTTPError as e:
            # Device responded but with bad status
            print(f"[fetch] HTTP error: {e}")
            raise
        finally: # Ensure session is closed no matter what happens above
            session.close()
    else:
        # ran out of retries
        raise RuntimeError("Unable to connect to MKII after retries")
    # ---- Parsing (unchanged, but now safe) ----
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)
    varList = text.split('\n')
    try:
        air_temp_DegF = varList[17]
        humidity_Percent = varList[30]
        barometric_pressure_InHg = varList[43]
        wind_MiPHr_DegCompass = varList[56]   # speed and direction separated by a comma
        precipitation_In = varList[65]
        solar_radiation_WPM2 = varList[70]
    except Exception:
        raise IndexError(f'Unexpected HTML format, varList length: {len(varList)}')
    data = str(time()) + ', ' + air_temp_DegF + ', ' + humidity_Percent + ', ' \
        + barometric_pressure_InHg + ', ' + wind_MiPHr_DegCompass + ', ' + precipitation_In \
        + ', ' + solar_radiation_WPM2
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
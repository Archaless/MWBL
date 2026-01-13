###########################################################################
               ### Config for SMAST DPL ###
###########################################################################
# Python Libraries
import os
from time import time
# Local Libraries
from Serial_Scripts import connect2serial
from Helper_Scripts import sync_Clock

###########################################################################
                    ### Global Variables for log_main ###
###########################################################################

REQUIRED = ['connection','savePath'] # DO NOT REMOVE
# Misc
backupDays = 60 # Days
retryAttempts = 3
logTime = 'daily' # 'hourly' or 'daily'
connection = [0x0483, 0x5740] # VID and PID (if serial), otherwise use int for eth# or -1 for wlan0
# Save Location Config:
savePath = '/home/pi/Data/DPL/' # Local directory to upload
tmpPath = '/home/pi/Data/DPL-tmp/' # Local directory to write data (will be moved to savePath after start of next file)
logPath = '/home/pi/log.txt' # Local directory to store log file
# Remote Machine Config:
hostname_Transfer = '192.168.2.1' # IP Address
username_Transfer = 'pi' # Username
transferPath = '/home/pi/Bookshelf/Desktop/Tower_SMAST/' # Location to transfer saves to
# Filename Config:
titlePre = 'DPL_SMAST_210911_Data_'
titlePost = '.txt'
# File Header:
header = '10\tRecordNo\tStatusFlags\tDateTime\tUdemod\tUdemodSig\tCn2\tCn2Sig\t' \
            'Cn2Min\tCn2Max\tSrt\tHfree\tDeviceTemp\tAirTemp\tAirPressure\t' \
            'WindSpeed\n[-]\t[-]\t[-]\t[yy/mm/dd hh:mm:ss]\t[mV]\t[mV]\t[m^-2/3]\t' \
            '[m^-2/3]\t[m^-2/3]\t[m^-2/3]\t[K^2/m^2/3]\t[W/m²]\t[°C]\t[°C]\t' \
            '[mBar]\t[m/s]\n'

###########################################################################
                     ### Global Variables for below ###
###########################################################################
# Serial Config Settings:
baud = 115200 # Bits per second
vid = 0x0483 # DPL
pid = 0x5740 # DPL

###########################################################################
                           ### Functions ###
###########################################################################

def fetch(serialStream):
    data = parse_Data(serialStream.readline())
    return data

def init(logger):
    # Connecting:
    serialStream = connect2serial(connection, logPath, baudRate=baud)
    logger.info(f'Opened serial port: {connection}', logPath)
    print('Syncing Pi Clock')
    os.sys('date') #sync_Clock(hostname_Transfer, username_Transfer)
    data = parse_Data(serialStream.readline())
    if data == None:
        raise ValueError(f'Failed status check of device: {vid}:{pid}')
    logger.info(f'Successful status of device: {vid}:{pid}')
    return serialStream # Whatever is returned will be passed to fetch 
    # i.e. (filePath, *args) where *args is everything returned above

###########################################################################
                           ### Helper Functions ###
###########################################################################

def parse_Data(dataLine):
    data = dataLine.decode('utf-8', errors='replace').strip()
    if 'ERROR' in data:
        raise ValueError('ERROR: In KZS config function parse_Data - Command not found.')
    if data == '':
        return None
    return data
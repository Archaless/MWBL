###########################################################################
                      ### Config for CBC Lattice ###
###########################################################################
# Python Libraries
import os
from time import time
# Local Libraries
from Serial_Scripts import connect2serial
from Helper_Scripts import sync_Clock

###########################################################################
                ### Global Variables for transfer_data.py ###
###########################################################################


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
    sync_Clock(hostname, username)
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
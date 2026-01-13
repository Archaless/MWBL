###########################################################################
               ### Config for SMAST K&Z Scintillometer ###
###########################################################################
# Python Libraries
from time import time
# Local Libraries
from Serial_Scripts import connect2serial
###########################################################################
                       ### Global Variables ###
###########################################################################

REQUIRED = ['device','connection','savePath'] # DO NOT REMOVE
# Misc
device = 'KZS'
backupDays = 30 # Days
retryAttempts = 3
logTime = 'daily' # 'hourly' or 'daily'
connection = [0x06cd,0x0121] # VID and PID (if serial), otherwise use int for eth# or -1 for wlan0
# Save Location Config:
savePath = '/home/pi/Data/KZS/' # Local directory to upload
tmpPath = '/home/pi/Data/KZS-tmp/' # Local directory to write data (will be moved to savePath after start of next file)
logPath = '/home/pi/' # Local directory to store log file
logFilename = 'KZS_log.txt'
# Remote Machine Config:
hostname = '192.168.0.1' # IP Address
username = 'KZLocal' # Username
remotePath = 'C:/Users/KZLocal/Documents/KZ_Scintillometer/Data/' # Location to transfer saves to
# Filename Config:
titlePre = ''
titlePost = '_120026.log'
# File Header:
header = '10\tRecordNo\tStatusFlags\tDateTime\tUdemod\tUdemodSig\tCn2\tCn2Sig\t' \
            'Cn2Min\tCn2Max\tSrt\tHfree\tDeviceTemp\tAirTemp\tAirPressure\t' \
            'WindSpeed\n[-]\t[-]\t[-]\t[yy/mm/dd hh:mm:ss]\t[mV]\t[mV]\t[m^-2/3]\t' \
            '[m^-2/3]\t[m^-2/3]\t[m^-2/3]\t[K^2/m^2/3]\t[W/m²]\t[°C]\t[°C]\t' \
            '[mBar]\t[m/s]\n'

###########################################################################
                       ### Local Variables ###
###########################################################################
# Serial Config Settings:
baud = 19200 # Bits per second
vid = 0x06cd
pid = 0x0121
timeout = 2 # Seconds, how long to wait for a response from sensor

###########################################################################
                           ### Functions ###
###########################################################################

def fetch(serialStream):
    data = send_serial(serialStream, '.cont;')
    return data

def init(logger):
    # Connecting:
    serialStream = connect2serial(vid, pid, logger, baudRate=baud, timeout=timeout)
    serialStream.reset_input_buffer()
    serialStream.reset_output_buffer()
    data = send_serial(serialStream,'.get status;')
    if data == None:
        raise ValueError(f'Failed status check of device: {vid}:{pid}')
    logger.info(f'Successful status of device: {vid}:{pid}')
    send_serial(serialStream,'.stop=0;.play=1;') # Tell Scint to start serial stream
    return serialStream # Whatever is returned will be passed to fetch

def cleanup(serialStream): # Must have same args as init
    send_serial(serialStream,'.stop=1;') # Tell Scint to stop serial stream
    serialStream.reset_input_buffer()
    serialStream.reset_output_buffer()
    serialStream.close()

###########################################################################
                           ### Helper Functions ###
###########################################################################
def parse_Data(dataLine):
    data = dataLine.decode('utf-8', errors='replace').strip()
    if 'ERROR' in data:
        raise ValueError('ERROR: In KZS config function parse_Data - Command not found.')
    # Replace Misc chars and strings from message
    ### DEBUGGING ###
    data_raw = data
    with open('/home/pi/Data/KZS_debug.txt','a') as file:
        file.write(f'{data_raw}\n')
    ### DEBUGGING ###
    data = data.replace('.DATA=','').replace('.OK;','').replace("b'","").replace("'","").replace(';','\t')
    data = data.split('.DONE=',1)[0] # Removes everything after '.DONE='
    if data == '' or len(data) < 50:
        return None
    return data

def send_serial(serialStream, msg):
    # Send Message
    serialStream.write(f'{msg}\n\r'.encode())
    # Collect Response
    data = ''
    data_nm1 = ''
    timeMax = time() + timeout
    dataTmp = parse_Data(serialStream.readline())
    while (not dataTmp == None) and (time() < timeMax):
        if not dataTmp == data_nm1:
            data += dataTmp
        data_nm1 = dataTmp
        dataTmp = parse_Data(serialStream.readline())
    if data == '':
        data = None
    return data
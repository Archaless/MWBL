import os
import math
import threading
from time import time, sleep
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import *

from Serial_Scripts import restart_Serial
from Network_Scripts import restart_Network, sftp_IsFile
###########################################################################
                      ### General Functions ###
###########################################################################
# Add '0' to data/time, i.e. in: '3' out: '03' | in: '12' out: '12'
def add_PreZero(string):
    if len(string) == 1:
        string = '0' + string
    return string

# Appends a number to filename if file already exists
def append_Num(filepath, sftp=None):
    fileExists = True # Assume True until checked
    itr = 0
    fileName = get_PostFix(filepath)
    while fileExists:
        if itr > 0:
            if itr == 1:
                fileName[0] += '_' + str(itr)
            else:
                fileName[0] = fileName[0][:-len(str(itr-1))] + str(itr)
        filepath = fileName[0] + '.' + fileName[1] # Update filepath w/appended file extension
        fileExists = is_File(filepath, sftp)
        itr += 1
    return filepath

def get_PostFix(filename):
    if '.' in filename:
        parts = filename.rsplit('.', 1)
        return parts # Return filename and extension
    else:
        return ''

# Returns 1 if file doesn't exist AND if file is active, otherwise returns 0
def is_File_Active(filepath,sftp=None):
    if sftp:
        if sftp_IsFile(filepath, sftp):
            sizePre = sftp.stat(filepath).st_size
        else:
            return 1
    else:
        if os.path.isfile(filepath):
            sizePre = os.path.getsize(filepath)
        else:
            return 1
    sleep(3) # Wait for file to be written to
    if sftp: 
        sizePost = sftp.stat(filepath).st_size
    else:
        sizePost = os.path.getsize(filepath)
    if sizePre == sizePost:
        return 0
    else:
        return 1

def is_File(filepath, sftp=None):
    if sftp:
        return sftp_IsFile(filepath, sftp)
    else:
        return os.path.isfile(filepath)

def loading_Bar(lastTime):
    # Use in for/while loop
    # ex: 
    # lastTime = time()
    # for x in list
    #   ...
    #   lastTime = loading_bar(lastTime)
    dt = time() - lastTime
    if dt <= 4:
        print('logging' + '.' * math.floor(dt), end='\r')
    else:
        print('logging' + ' ' * 5, end='\r')
        return time()
    return lastTime

def make_Title(titlePre,titlePost,format):
    currentTime = datetime.now(timezone.utc)
    month = add_PreZero(str(currentTime.month))
    day = add_PreZero(str(currentTime.day))
    if format == 'hourly' or format == 'test':
        hour = add_PreZero(str(currentTime.hour))
        minute = add_PreZero(str(currentTime.minute))
        second = add_PreZero(str(currentTime.second))
        titleTime = str(currentTime.year) + month + day + '-' + hour + minute + second
    else:
        titleTime = str(currentTime.year) + month + day
    # Construct filename
    title = titlePre + titleTime + titlePost
    return title

def offset_Days(minusDays):
    # Below for use with datetime only
    date = datetime.now()
    date_corrected = date - timedelta(days=minusDays) # Remove desired number of days
    dateFormated = datetime(year=date_corrected.year, month=date_corrected.month, day=date_corrected.day)
    return dateFormated

# Helps print file transfer progess to/from. Cannot be used with http pull
def print_Totals(transferred, toBeTransferred):
    print('\rTransferred: {0}\tOut of: {1}'.format(transferred,toBeTransferred),end='')

def make_Dir(path, sftp=False):
    if sftp:
        if not is_File(path, sftp): sftp.mkdir(path)
    else:
        os.makedirs(path, exist_ok=True)

def reboot_Sys():
    # Try to reboot the system to recover from unknown critical failures.
    # Keep this behavior but make it safer by attempting to sync logs first.
    try:
        with open('./.numRestart','r') as file:
            num_restart = len(file.read())
    except:
        num_restart = 0
    # Check number of restarts
    if num_restart >= 3:
        return 2
    else:
        num_restart += 1
        with open('./.numRestart','w') as file:
            file.write(num_restart*'1')
    # Reboot
    reboot = threading.Thread(target=os.system('sudo reboot'))
    reboot.start()
    sleep(5)

def retry_Logic(connection, retryAttempts, logger, func, *args, **kwargs):
    # Inputs:
    #   connection - 0,1,2,3... will rebooth eth0/1/2/3...
    #              - -1 will reboot wlan0
    #              - *any pair of int* ex. [0x0d6c 0x0121] will reboot serial device
    #   logPath
    #   retryAttempts
    #   func - function to call
    #   *args, **kwargs - arguments to pass to func
    attempt = 1
    while True:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Use sync to flush disks
            try:
                os.system('sync')
            except:
                pass
            logger.warning(f"Retrying after {attempt}/{retryAttempts} attempts due to: {e}")
            # Attempt a network restart
            try:
                if len(connection) == 1:
                    restart_Network(connection)
                else:
                    restart_Serial(connection)
            except Exception:
                logger.error(f'Failed to reboot network: {connection}')
            # Reboot
            if attempt >= retryAttempts:
                # Reboot
                reboot_Sys()
                # If above fails/timesout, throw error and exit
                raise RuntimeError('UNABLE TO REBOOT')
            # Give System time to rest
            sleep(3)
        attempt += 1

def sync_Clock(hostname, username):
    os.system(f'remote_time=`ssh {username}@{hostname} date +"%Y-%m-%dT%H:%M:%S"` && sudo date -s "$remote_time"')
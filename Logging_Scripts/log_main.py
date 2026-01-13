# Log data from sensor specified in config.py
# NOTE: config.py, Data_Transfer_Scripts.py, Helper_Scripts.py, and any other
# local libraries must be in the same folder as log_main.py

# Crontab setup:
# @reboot sleep 20 && python3 /home/pi/Scripts/log_main.py

# Created by Tyler Knapp 11/06/2025

# Python Libraries
import os
import sys
import logging
import traceback
from time import time # Always use time() as timestamp (if needed)
from datetime import datetime, timedelta, timezone
# Local Libraries
import config
from Helper_Scripts import retry_Logic, make_Title, loading_Bar, reboot_Sys
from Data_Transfer_Scripts import folder2folder
from Test_Suite import system_Health_Check

###########################################################################
                           ### Config Defaults ###
###########################################################################

# Default values for non-essential config variables
DEFAULTS = {
    "backupDays": 30,
    "retryAttempts": 3,
    "logTime": 'daily',
    "tmpPath": config.savePath[0:-1]+'-tmp/',
    "logPath": config.savePath[0:-1]+'-log/',
    "titlePre": 'data_',
    "titlePost": '.txt',
    "header": '',
    "runTests": True,
    "logFilename": "log.txt"
}

# Set missing config variables to default values
def apply_defaults():
    for name, value in DEFAULTS.items():
        if not hasattr(config, name) or value == None \
                        or (type(value) == 'string' and len(value) == 0):
            setattr(config, name, value)
    if not (config.logTime == 'daily' or config.logTime == 'hourly' or\
             config.logTime == 'test'):
        logger.warning(f'logTime not recognized use "hourly" or "daily"\n\
                       \tDefaulting to: "{DEFAULTS["logTime"]}"')
        # Override 'logTime' in config.py with default value
        setattr(config, 'logTime', DEFAULTS['logTime'])

# Run above function
apply_defaults()

###########################################################################
                           ### Logger Setup ###
###########################################################################

# Initalize python logger, will append log.txt in logPath
logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.logPath+config.logFilename, \
    encoding='utf-8', level=logging.INFO,format='%(asctime)s %(message)s',\
    datefmt='%m/%d/%Y %I:%M:%S %p')

###########################################################################
                           ### Functions ###
###########################################################################

def log(filePath, endTime, init_args):
    lastTime = time()
    while time() < endTime:
        data = config.fetch(init_args)
        if not data == None and len(data) > 0:
            with open(filePath, 'a') as file:
                if data[-1:] == '\n':
                    data = data[0:-1] # Strip last newline if present
                file.write(f'{data}\n')
        lastTime = loading_Bar(lastTime)
    config.cleanup(init_args) # At end of logging interval cleanup connection
    return 0

def log_Init(startTime=None,attempts=0):
    if startTime == None:
        # Setting this outside of def line or else it wont update to present time
        startTime = datetime.now(timezone.utc)
    # Calculate the start of the next logging interval
    # Timedelta avoids errors when incrementing days and months
    if config.logTime == 'hourly':
        # Add an hour and zero out minutes, seconds, and microseconds
        dt = timedelta(hours=1, minutes=-startTime.minute, \
                        seconds=-startTime.second, microseconds=-startTime.microsecond)
    elif config.logTime == 'daily':
        # Add a day and zero out hours, minutes, seconds, and microseconds
        dt = timedelta(days=1, hours=-startTime.hour, minutes=-startTime.minute,\
                        seconds=-startTime.second, microseconds=-startTime.microsecond)
    elif config.logTime == 'test':
        dt = timedelta(seconds=5)
    else:
        ValueError('ERROR: in log_main config variable "logTime" not recognized')
    endTime = startTime + dt
    # Make title based on timestamp
    title = make_Title(config.titlePre,config.titlePost,config.logTime)
    tmpFilePath = os.path.join(config.tmpPath, title)
    # Log title, name of output file cration, and next file time
    logger.info(f'{title} Start: {startTime} End: {endTime}')
    # Check if file exits and create with header if not
    if not os.path.isfile(tmpFilePath):
        # Write header to file
        with open(tmpFilePath, 'w') as file:
            file.write(config.header)
        logger.info(f'Successfully Created Data File: {tmpFilePath}')
    return [tmpFilePath, endTime]

###########################################################################
                                ### Main ###
###########################################################################

def main(argv=None):
    os.makedirs(config.savePath, exist_ok=True)
    os.makedirs(config.tmpPath, exist_ok=True)
    os.makedirs(config.logPath, exist_ok=True)
    try:
        if config.runTests and not system_Health_Check(logger):
            return 2
    except: # Catch if system_Health_Check itself fails
        pass
    while True:
        try:
            [tmpFilePath, endTime] = retry_Logic(None, config.retryAttempts, \
                                                    logger, log_Init)
            init_args = retry_Logic(None, config.retryAttempts, \
                                        logger, config.init, logger)
            # log runs until endTime; '.timestamp()' returns time() format
            retry_Logic(config.connection, config.retryAttempts, \
                            logger, log, tmpFilePath, endTime.timestamp(), init_args)
            with open('./.numRestart','w') as file:
                file.write('') # Reset restart attempts
            folder2folder(config.tmpPath, None, config.savePath, None, logger)
        except KeyboardInterrupt:
            return 1
        except Exception:
            # Only used if retry_Logic throws an error
            try:
                config.cleanup(logger, init_args)
            except:
                pass
            error = traceback.format_exc()
            print(f'Exiting main due to: {error}')
            logger.critical(f'Exiting main due to: {error}')
            reboot_Sys()
            return 2

if __name__ == '__main__':
    sys.exit(main())

import sys
import logging
import traceback
from time import time
from Helper_Scripts import sync_Clock
from HTTP_Scripts import get_DataQ
from Network_Scripts import sftp_Server
from Data_Transfer_Scripts import folder2folder, backup_Folder

# Created by Tyler Knapp 12/01/2025 for CBC Lattice
###########################################################################
                           ### Logger Setup ###
###########################################################################

logPath = '/home/pi/log.txt'
# Initalize python logger, will append log.txt in logPath
logger = logging.getLogger(__name__)
logging.basicConfig(filename=logPath, \
    encoding='utf-8', level=logging.INFO,format='%(asctime)s %(message)s', \
    datefmt='%m/%d/%Y %I:%M:%S %p')

###########################################################################
                         ### Global Variables ###
###########################################################################
# DataQ
hostname_DataQ = '192.168.1.22'
username_DataQ = 'admin'
password_DataQ = 'admin'
localPath_DataQ = '/home/pi/Data/DataQ/'
localBackup_DataQ = '/home/pi/Data/DataQ-backup/'
sourcePath_DataQ = '/data/files/local/'
transferPath_DataQ = '/usr2/MWBL/Data/Lattice_CBC_Station2/DataQ/raw/'
numFiles = 14 # Number of files pulled, 1 will download 2 days ago, 2 will
              # download 2&3 days ago, and so on. -1 will check and download ALL DataQ files
# ATI
localPath_ATI = '/home/pi/Data/ATI/'
localBackup_ATI = '/home/pi/Data/ATI-backup/'
sourcePath_ATI = '/home/pi/Desktop/SMAST_WeatherStation2/Station2_Data/ATI_Anemometer/'
transferPath_ATI = '/usr2/MWBL/Data/Lattice_CBC_Station2/ATI/raw/'
# Enclosure Temp
localPath_ET = '/home/pi/Data/EnclosureTemp/'
localBackup_ET = '/home/pi/Data/EnclosureTemp-backup/'
sourcePath_ET = '/home/pi/Desktop/SMAST_WeatherStation2/Station2_Data/Enclosure_Temperature_Sensor/'
transferPath_ET = '/usr2/MWBL/Data/Lattice_CBC_Station2/EnclosureTemp/raw/'
# Campbell Box
hostname_Source = '192.168.1.20'
username_Source = 'pi'
# MWBL
hostname_Transfer = '192.168.0.30'
username_Transfer = 'MWBL'
password_Transfer = None
# Date (sec. from epoch) of final desired backup file
backupEnd = time() - 24*60*60 * 60

def main(argv=None):
    try:
        # Sync clock with Lattice Pi
        sync_Clock(hostname_Source, username_Source)
        print('~~~ Initializing File Transfer ~~~')
        print('Pulling/Pushing DataQ')
        get_DataQ(hostname_DataQ, username_DataQ, password_DataQ, localPath_DataQ, localBackup_DataQ,
                    sourcePath_DataQ, transferPath_DataQ, hostname_Transfer,
                    username_Transfer, password_Transfer, numFiles, logger)
        # Pull source data:
        sftp_Source = sftp_Server(hostname_Source, username_Source)
        sftp_Local = None
        print('Pulling ATI')
        folder2folder(sourcePath_ATI, sftp_Source, localPath_ATI, sftp_Local, logger)
        backup_Folder(sourcePath_ATI, sftp_Source, localBackup_ATI, backupEnd, logger)
        print('Pulling Enclosure Temp')
        folder2folder(sourcePath_ET, sftp_Source, localPath_ET, sftp_Local, logger)
        backup_Folder(sourcePath_ET, sftp_Source, localBackup_ET, backupEnd, logger)
        sftp_Transfer = sftp_Server(hostname_Transfer, username_Transfer)
        print('Pushing ATI')
        folder2folder(localPath_ATI, sftp_Local, transferPath_ATI, sftp_Transfer, logger)
        backup_Folder(localPath_ATI, sftp_Local, localBackup_ATI, backupEnd, logger)
        print('Pushing Enclosure Temp')
        folder2folder(localPath_ET, sftp_Local, transferPath_ET, sftp_Transfer, logger)
        backup_Folder(localPath_ET, sftp_Local, localBackup_ET, backupEnd, logger)
        print('~~~ Transfer Completed! ~~~')
    except KeyboardInterrupt:
        return 1
    except Exception:
        error = traceback.format_exc()
        print(f'Exiting main due to: {error}')
        logger.critical(f'Exiting main due to: {error}')
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())

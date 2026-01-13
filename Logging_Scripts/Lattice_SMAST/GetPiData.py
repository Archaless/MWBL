import sys
import logging
import traceback
from time import time

from Helper_Scripts import sync_Clock, is_File
from HTTP_Scripts import get_DataQ
from Network_Scripts import connect2sys, sftp_Server, sftp_Server_wPass
from Data_Transfer_Scripts import folder2folder, backup_Folder

from rename_DPL_files import rename_DPL

# Created by Tyler Knapp 12/10/2025 for SMAST Lattice
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
hostname_DataQ = '192.168.1.11'
username_DataQ = 'admin'
password_DataQ = 'admin'
localPath_DataQ = '/home/pi/Data/DataQ/'
localBackup_DataQ = '/home/pi/Data/DataQ-backup/'
sourcePath_DataQ = '/data/files/local/'
numFiles = 14 # Number of files pulled, 1 will download 2 days ago, 2 will
              # download 2&3 days ago, and so on. -1 will check and download ALL DataQ files
# ATI
localPath_ATI = '/home/pi/Data/ATI/'
localBackup_ATI = '/home/pi/Data/ATI-backup/'
sourcePath_ATI = '/home/pi/Desktop/SMAST_Station1_Data/ATIAnemometer/'
# Gill
localPath_Gill = '/home/pi/Data/Gill/'
localBackup_Gill = '/home/pi/Data/Gill-backup/'
sourcePath_Gill = '/home/pi/Desktop/SMAST_Station1_Data/GillAnemometer/'
# Enclosure Temp
localPath_ET = '/home/pi/Data/EnclosureTemp/'
localBackup_ET = '/home/pi/Data/EnclosureTemp-backup/'
sourcePath_ET = '/home/pi/Desktop/SMAST_Station1_Data/EnclosureTemperatureSensor/'
# Tower
localPath_Tower = '/home/pi/Data/Tower_SMAST/'
localBackup_Tower = '/home/pi/Data/Tower_SMAST-backup/'
sourcePath_Tower = '/home/pi/Desktop/Tower_SMAST/'
# Campbell Box
hostname_Source = '192.168.1.10'
username_Source = 'pi'
# Miles PC
hostname_Transfer = '192.168.1.50'
username_Transfer = 'MWBL'
password_Transfer = 'metdata2025!!'
# Date (sec. from epoch) of final desired backup file
backupEnd = time() - 24*60*60 * 60

def main(argv=None):
    try:
        connect2sys(hostname_Source)
        # Sync clock with Lattice Pi
        sync_Clock(hostname_Source, username_Source)
        print('~~~ Initializing File Transfer ~~~')
        # Check if MWBL is properly mounted on Miles PC
        connect2sys(hostname_Transfer)
        sftp = sftp_Server_wPass(hostname_Transfer,username_Transfer,password_Transfer)
        if is_File('/mnt/MWBL/Data'):
            # Transfer files to MWBL via Miles' PC
            transferPath_DataQ = '/mnt/MWBL/Data/Lattice_SMAST_Station1/DataQ/raw/'
            transferPath_ATI = '/mnt/MWBL/Data/Lattice_SMAST_Station1/ATI/raw/'
            transferPath_Gill = '/mnt/MWBL/Data/Lattice_SMAST_Station1/Gill/raw/'
            transferPath_ET = '/mnt/MWBL/Data/Lattice_SMAST_Station1/EnclosureTemp/raw/'
            transferPath_Tower = '/mnt/MWBL/Data/DPL_SMAST/raw/'
            dest = 'MWBL'
        else:
            # Transfer files to Miles' PC
            transferPath_DataQ = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/DataQ/'
            transferPath_ATI = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/ATI/'
            transferPath_Gill = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/Gill/'
            transferPath_ET = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/EnclosureTemp/'
            transferPath_Tower = '/usr4/MWBL/Data_xfer/Tower_SMAST/'
            dest = 'Miles PC'
        print(f'Files will be transferred to: {dest}')
        # Pull source data:
        sftp_Source = sftp_Server(hostname_Source, username_Source)
        sftp_Local = None
        print('Pulling/Pushing DataQ')
        get_DataQ(hostname_DataQ, username_DataQ, password_DataQ, localPath_DataQ,
                   localBackup_DataQ, sourcePath_DataQ, transferPath_DataQ, 
                   hostname_Transfer, username_Transfer, password_Transfer,
                   numFiles, logger)
        connect2sys(hostname_Source)
        print('Pulling ATI')
        folder2folder(sourcePath_ATI, sftp_Source, localPath_ATI, sftp_Local, logger)
        backup_Folder(sourcePath_ATI, sftp_Source, localBackup_ATI, backupEnd, logger)
        print('Pulling Gill')
        folder2folder(sourcePath_Gill, sftp_Source, localPath_Gill, sftp_Local, logger)
        backup_Folder(sourcePath_Gill, sftp_Source, localBackup_Gill, backupEnd, logger)
        print('Pulling Enclosure Temp')
        folder2folder(sourcePath_ET, sftp_Source, localPath_ET, sftp_Local, logger)
        backup_Folder(sourcePath_ET, sftp_Source, localBackup_ET, backupEnd, logger)
        print('Pulling Tower')
        folder2folder(sourcePath_Tower, sftp_Source, localPath_Tower, sftp_Local, logger)
        backup_Folder(sourcePath_Tower, sftp_Source, localBackup_Tower, backupEnd, logger)
        rename_DPL() # Rename DPL files with f_open error
        connect2sys(hostname_Transfer)
        sftp_Transfer = sftp_Server_wPass(hostname_Transfer, username_Transfer, password_Transfer)
        print('Pushing ATI')
        folder2folder(localPath_ATI, sftp_Local, transferPath_ATI, sftp_Transfer, logger)
        backup_Folder(localPath_ATI, sftp_Local, localBackup_ATI, backupEnd, logger)
        print('Pushing Gill')
        folder2folder(localPath_Gill, sftp_Local, transferPath_Gill, sftp_Transfer, logger)
        backup_Folder(localPath_Gill, sftp_Local, localBackup_Gill, backupEnd, logger)
        print('Pushing Enclosure Temp')
        folder2folder(localPath_ET, sftp_Local, transferPath_ET, sftp_Transfer, logger)
        backup_Folder(localPath_ET, sftp_Local, localBackup_ET, backupEnd, logger)
        print('Pushing Tower')
        folder2folder(localPath_Tower, sftp_Local, transferPath_Tower, sftp_Transfer, logger)
        backup_Folder(localPath_Tower, sftp_Local, localBackup_Tower, backupEnd, logger)
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
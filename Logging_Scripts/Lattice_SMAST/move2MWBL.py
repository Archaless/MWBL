# File to attempt to move files from Miles' PC to MWBL
# functions as a backup if folder is not mounted on Miles PC
# Created by Tyler Knapp 01/05/2026 for CBC Lattice
logPath = '/usr4/MWBL/log.txt'

import sys
import logging
import traceback
from time import time
from Helper_Scripts import is_File
from Network_Scripts import  sftp_Server_wPass
from Data_Transfer_Scripts import folder2folder, backup_Folder
###########################################################################
                           ### Logger Setup ###
###########################################################################
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
localPath_DataQ = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/DataQ/'
localBackup_DataQ = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/DataQ-backup/'
# ATI
localPath_ATI = '/usr4/MWBL/Data_xfer/ATI/'
localBackup_ATI = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/ATI-backup/'
# Gill
localPath_Gill = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/Gill/'
localBackup_Gill = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/Gill-backup/'
# Enclosure Temp
localPath_ET = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/EnclosureTemp/'
localBackup_ET = '/usr4/MWBL/Data_xfer/Lattice_SMAST_Station1/EnclosureTemp-backup/'
# Tower
localPath_Tower = '/usr4/MWBL/Data_xfer/Tower_SMAST/'
localBackup_Tower = '/usr4/MWBL/Data_xfer/Tower_SMAST-backup/'
# MWBL PC
hostname_Transfer = '134.88.228.141'
username_Transfer = 'MWBL'
password_Transfer = 'metdata2025!!'
# Date (sec. from epoch) of final desired backup file
backupEnd = time() - 24*60*60 * 60

def main(argv=None):
    try:
        if is_File('/mnt/MWBL/Data'): # Check if MWBL is properly mounted on Miles PC
            sftp_Transfer = None
            transferPath_DataQ = '/mnt/MWBL/Data/Lattice_SMAST_Station1/DataQ/raw/'
            transferPath_ATI = '/mnt/MWBL/Data/Lattice_SMAST_Station1/ATI/raw/'
            transferPath_Gill = '/mnt/MWBL/Data/Lattice_SMAST_Station1/Gill/raw/'
            transferPath_ET = '/mnt/MWBL/Data/Lattice_SMAST_Station1/EnclosureTemp/raw/'
            transferPath_Tower = '/mnt/MWBL/Data/DPL_SMAST/raw/'
        else:
            sftp_Transfer = sftp_Server_wPass(hostname_Transfer, username_Transfer, password_Transfer)
            transferPath_DataQ = '/usr2/MWBL/Data/Lattice_SMAST_Station1/DataQ/raw/'
            transferPath_ATI = '/usr2/MWBL/Data/Lattice_SMAST_Station1/ATI/raw/'
            transferPath_Gill = '/usr2/MWBL/Data/Lattice_SMAST_Station1/Gill/raw/'
            transferPath_ET = '/usr2/MWBL/Data/Lattice_SMAST_Station1/EnclosureTemp/raw/'
            transferPath_Tower = '/usr2/MWBL/Data/DPL_SMAST/raw/'
        sftp_Local = None
        print('Pushing DataQ')
        folder2folder(localPath_DataQ, sftp_Local, transferPath_DataQ, sftp_Transfer, logger)
        backup_Folder(localPath_DataQ, sftp_Local, localBackup_DataQ, backupEnd, logger)
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
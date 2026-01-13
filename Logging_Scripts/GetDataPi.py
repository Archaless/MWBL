from Data_Transfer_Scripts import folder2folder, backup_Folder
from Network_Scripts import sftp_Server_wPass
from time import time
import traceback
import logging
import sys

###########################################################################
                           ### Logger Setup ###
###########################################################################
logPath = 'C:/Users/KZLocal/Documents/log.txt'
# Initalize python logger, will append log.txt in logPath
logger = logging.getLogger(__name__)
logging.basicConfig(filename=logPath, \
    encoding='utf-8', level=logging.INFO,format='%(asctime)s %(message)s', \
    datefmt='%m/%d/%Y %I:%M:%S %p')

# MWBL SFTP server details
hostname_Transfer = '134.88.228.141'
username_Transfer = 'MWBL'
password_Transfer = 'metdata2024!!'
# PI SFTP server details
hostname_Source = '192.168.0.3'
username_Source = 'pi'
password_Source = 'cdepi'
# K&Z Scintillometer
localPath_KZS = 'C:/Users/KZLocal/Documents/Data/KZS/'
sourcePath_KZS = '/home/pi/Data/KZS/'
localBackup_KZS = 'C:/Users/KZLocal/Documents/Data/KZS-backup/'
sourceBackup_KZS = '/home/pi/Data/KZS-backup/'
transferPath_KZS = '/usr2/MWBL/Data/KZScintillometer/raw/'
# Rainwise MKIII
localPath_MKIII = 'C:/Users/KZLocal/Documents/Data/MKIII/'
sourcePath_MKIII = '/home/pi/Data/MKIII/'
localBackup_MKIII = 'C:/Users/KZLocal/Documents/Data/MKIII-backup/'
sourceBackup_MKIII = '/home/pi/Data/MKIII-backup/'
transferPath_MKIII = '/usr2/MWBL/Data/RainwisePortLog/raw/'
# Date (sec. from epoch) of final desired backup file
backupEnd = time() - 24*60*60 * 60

def main(argv=None):
    try:
        print('~~~ Initializing File Transfer ~~~')
        sftp_Source = sftp_Server_wPass(hostname_Source, username_Source, password_Source)
        sftp_Local = None
        # Scintillometer Transfer
        print('Pulling Scintillometer')
        folder2folder(sourcePath_KZS, sftp_Source, localPath_KZS, sftp_Local, logger)
        backup_Folder(sourcePath_KZS, sftp_Source, localBackup_KZS, backupEnd, logger)
        # MKIII Transfer
        print('Pulling MKIII')
        folder2folder(sourcePath_MKIII, sftp_Source, localPath_MKIII, sftp_Local, logger)
        backup_Folder(sourcePath_MKIII, sftp_Source, localBackup_MKIII, backupEnd, logger)
        sftp_Transfer = sftp_Server_wPass(hostname_Transfer, username_Transfer, password_Transfer)
        # Scintillometer Transfer
        print('Pushing Scintillometer')
        folder2folder(localPath_KZS, sftp_Local, transferPath_KZS, sftp_Transfer, logger)
        backup_Folder(localPath_KZS, sftp_Local, localBackup_KZS, backupEnd, logger)
        # MKIII Transfer
        print('Pushing MKIII')
        folder2folder(localPath_MKIII, sftp_Local, transferPath_MKIII, sftp_Transfer, logger)
        backup_Folder(localPath_MKIII, sftp_Local, localBackup_MKIII, backupEnd, logger)
        print('~~~ Transfer Completed! ~~~')
    except KeyboardInterrupt:
        return 1
    except Exception:
        error = traceback.format_exc()
        logger.critical(f'Exiting main due to: {error}')
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
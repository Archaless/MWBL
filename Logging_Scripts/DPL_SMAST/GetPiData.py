import sys
import logging
import traceback
from time import time
from Network_Scripts import sftp_Server
from Data_Transfer_Scripts import folder2folder, clean_Up_Backup
# Created by Tyler Knapp 12/12/2025 for SMAST Lattice
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
# Tower
transferPath_Tower= '/home/pi/Data/Tower_SMAST/'
localPath_Tower = '/home/pi/Bookshelf/Desktop/Tower_SMAST/'
localBackup_Tower = '/home/pi/Bookshelf/Desktop/Tower_SMAST-backup/'
# Campbell Box
hostname_Transfer = '192.168.1.10'
username_Transfer = 'pi'
# Date (sec. from epoch) of final desired backup file
backupEnd = time() - 24*60*60 * 60

def main(argv=None):
    try:
        sftp_Transfer = sftp_Server(hostname_Transfer, username_Transfer)
        sftp_Local = None
        print('Pushing Tower')
        folder2folder(localPath_Tower, sftp_Local, transferPath_Tower, sftp_Transfer, logger)
        clean_Up_Backup(localBackup_Tower, backupEnd, logger)
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
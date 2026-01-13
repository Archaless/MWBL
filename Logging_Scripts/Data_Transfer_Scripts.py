# Created by Tyler Knapp 04/07/2025
# Updated for CBC Lattice file transfer 06/02/2025
# Updated for KZ file transfer 10/21/2025
# Seperating out Helper_Scripts, HTTP_Scripts, and Serial_Scripts, 10/29/2025

import os
from Helper_Scripts import is_File_Active, is_File, print_Totals, append_Num, make_Dir

###########################################################################
                    ### SFTP Transfer Functions ###
###########################################################################

# Remove backup files older than a certain date
def backup_Folder(sourcePath, sftp_Source, backupPath, backupEnd, logger=None):
    make_Dir(backupPath)
    folder2folder(sourcePath, sftp_Source, backupPath, None, logger, remove=True)
    print(f'Cleaning up backups older than: {backupEnd} in: {backupPath}')
    for filename in os.listdir(backupPath):
        backupFilepath = os.path.join(backupPath, filename)
        if not is_File(backupFilepath):
            print(f'File: {backupFilepath} is not a file, skipping')
            continue
        try:
            fileDate = os.stat(backupFilepath).st_mtime
        except Exception as e:
            print(f'Error moving backup: {str(e)}')
            if logger: logger.error(f'Error moving backup: {str(e)}')
            continue
        if fileDate < backupEnd:
            print(f'Deleting backup: {backupFilepath}')
            os.remove(backupFilepath)

# Function to transfer all files in local directory to remote directory, backup will always be a local diretory
def folder2folder(sourcePath, sftp_Source, transferPath, sftp_Transfer, logger=None, remove=False):
    # If source or transfer is local provide None as respective sftp
    make_Dir(sourcePath, sftp_Source)
    make_Dir(transferPath, sftp_Transfer)
    if sftp_Source:
        print('source remote')
        sourceMethod = sftp_Source
    else:
        print('source local')
        sourceMethod = os
    if sftp_Transfer:
        print('transfer remote')
        transferMethod = sftp_Transfer
    else:
        print('transfer local')
        transferMethod = os
    print(f'Attempting to move: {sourceMethod.listdir(sourcePath)}')
    for filename in sourceMethod.listdir(sourcePath):
        sourceFilepath = os.path.join(sourcePath, filename)
        if not is_File(sourceFilepath, sftp_Source):
            print(f'File: {sourceFilepath} is not a file, skipping')
            continue
        if is_File_Active(sourceFilepath, sftp_Source): # Will return 1 if active
            print(f'File: {sourceFilepath} is currently active, skipping')
            continue
        fileSize = sourceMethod.stat(sourceFilepath).st_size
        if fileSize == 0:
            print(f'File: {sourceFilepath} is empty (0 bytes), skipping')
            continue
        transferFilepath = os.path.join(transferPath, filename)
        if is_File(transferFilepath, sftp_Transfer) and \
                (sourceMethod.stat(sourceFilepath).st_size == transferMethod.stat(transferFilepath).st_size):
            print(f'File: {sourceFilepath} Already exists in: {transferFilepath}')
        else:
            transferFilepath = append_Num(transferFilepath, sftp_Transfer)
        print(f'Attempting to move: {sourceFilepath} to: {transferFilepath}')
        file2file(sourceFilepath, sftp_Source, transferFilepath, sftp_Transfer, logger)
        # Check if remote file exists and is the same size as local, paramiko SFTP doesn't always throw an error on failed transfers
        try:
            if is_File(transferFilepath, sftp_Transfer) and (fileSize == transferMethod.stat(transferFilepath).st_size):
                try:
                    if remove: sourceMethod.remove(sourceFilepath)
                except:
                    pass # Local to Local and Remote to Remote use rename removing the original copy
                print(f'Successful Transfer of: {sourceFilepath}')
            else:
                print(f'In folder2folder - Failed file transfer: {sourceFilepath}')
                if logger: logger.warning(f'In folder2folder - Failed file transfer: {sourceFilepath}')
        except:
            print(f'In folder2folder - Could not verify file transfer: {sourceFilepath}')
            if logger: logger.warning(f'In folder2folder - Could not verify file transfer: {sourceFilepath}')
            pass


def file2file(sourceFilepath, sftp_Source, transferFilepath, sftp_Transfer, logger=None):
    if sftp_Source:
        sourceMethod = sftp_Source
    else:
        sourceMethod = os
    if sftp_Transfer:
        transferMethod = sftp_Transfer
    else:
        transferMethod = os
    if is_File(transferFilepath, sftp_Transfer):
        if transferMethod.stat(transferFilepath).st_size == sourceMethod.stat(sourceFilepath).st_size:
            print(f'File: {sourceFilepath} Already exists in: {transferFilepath}')
    else:
        try:
            if sftp_Source and sftp_Transfer: # Remote to remote, won't preserve original
                sftp_Source.rename(sourceFilepath, transferFilepath)
            elif sftp_Source: # Remote to local
                sftp_Source.get(sourceFilepath, transferFilepath, callback=print_Totals, prefetch=True,
                                    max_concurrent_prefetch_requests=64)
                print('')
            elif sftp_Transfer: # Local to remote:
                sftp_Transfer.put(sourceFilepath, transferFilepath, callback=print_Totals, confirm=True)
                print('')
            else: # Local to Local, won't preserve original
                os.rename(sourceFilepath, transferFilepath)
        except Exception as e:
            print(f'In file2file - Error moving file: {str(e)}')
            if logger: logger.error(f'In file2file - Error moving file: {str(e)}')
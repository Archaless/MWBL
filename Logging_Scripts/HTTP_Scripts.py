import os
import requests
from time import time
from bs4 import BeautifulSoup
from requests.auth import HTTPDigestAuth
from Helper_Scripts import make_Dir, is_File
from Network_Scripts import sftp_Server, sftp_Server_wPass, sftp_IsFile
from Data_Transfer_Scripts import folder2folder, backup_Folder

###########################################################################
                      ### HTTP/DataQ Functions ###
###########################################################################
# Call all sub-functions to pull DataQ files
def get_DataQ(hostname_Source, username_Source, password_Source, localPath,
               localBackup, sourcePath, transferPath, hostname_Transfer,
               username_Transfer, password_Transfer, numFiles, logger):
    get_DataQ_Index(hostname_Source, username_Source, password_Source, 
                    localPath, sourcePath)
    filename_size = check_DataQ_Transfer(hostname_Transfer, username_Transfer,
                                          password_Transfer, transferPath, 
                                          localPath, numFiles, logger)
    filename = filename_size[0]
    size = filename_size[1]
    pull_DataQ(hostname_Source, username_Source, password_Source, localPath, 
               sourcePath, filename, size, logger)
    push_DataQ(hostname_Transfer, username_Transfer, password_Transfer,
                localPath, localBackup, transferPath, logger)

# Funtion to find filename from html filelist
def get_HTML_Info(htmlPath, numFiles):
    indexHTML = open(htmlPath)
    soupHTML = BeautifulSoup(indexHTML,'html.parser')
    names = soupHTML.find_all('span', class_='name')
    sizes = soupHTML.find_all('span', class_='size')
    # Start at index 1 to skip titles
    nameArray = [str(names[1]).replace('<span class="name">','').replace('</span>','')]
    sizeArray = [int(str(sizes[1]).replace('<span class="size">','').replace('</span>',''))]
    for itr in range(2,len(names)): # Insert value at beginning so order becomes new to old
        nameArray.insert(0,str(names[itr]).replace('<span class="name">','').replace('</span>',''))
        sizeArray.insert(0,int(str(sizes[itr]).replace('<span class="size">','').replace('</span>','')))
    if (numFiles > 0): # Return desired number of files
        return [nameArray[1:numFiles+1],sizeArray[1:numFiles+1]] # Add one to skip today's file
    else: # ex. numFiles = -1, Return all files (except today's)
        return [nameArray[1:],sizeArray[1:]] # Add one to skip today's file

def get_HTTP_File(hostname_Source, sourcePath, username_Source, password_Source, savePath):
    if not is_File(savePath):
        os.system(f'touch {savePath}')
    url = 'http://' + hostname_Source + sourcePath
    r = requests.get(url, auth=HTTPDigestAuth(username_Source, password_Source), timeout=60)
    if r.status_code == 200:
        with open(savePath, 'wb') as out:
            for bits in r.iter_content():
                out.write(bits)
            #End for
        #End with
    else:
        # Immediately throw an error, assume if this is hit it is a code error, not a network error
        raise ValueError(f'ERROR: Pulling http file: {url}, code: {str(r.status_code)}')

def get_DataQ_Index(hostname_Source, username_Source, password_Source,
                     localPath, sourcePath):
    make_Dir(localPath) # Data/DataQ
    make_Dir(os.path.join(localPath,'/tmp/')) # Data/DataQ/tmp
    # Pull index.html file
    get_HTTP_File(hostname_Source, sourcePath, username_Source, password_Source, 
                  os.path.join(localPath,'tmp/index.html'))
    # Read info from index.html

def check_DataQ_Transfer(hostname_Transfer, username_Transfer, password_Transfer, transferPath,
                            localPath, numFiles, logger):
    [filename, size] = get_HTML_Info(os.path.join(localPath,'tmp/index.html'), numFiles)
    itr = 0
    # Loop through files and check if they are already on remote pc
    while itr < len(filename):
        remoteFilepath = os.path.join(transferPath, filename[itr])
        if password_Transfer:
            sftp_Transfer = sftp_Server_wPass(hostname_Transfer, username_Transfer, password_Transfer)
        else:
            sftp_Transfer = sftp_Server(hostname_Transfer, username_Transfer)
        if sftp_IsFile(remoteFilepath, sftp_Transfer):
            if size[itr] == sftp_Transfer.stat(remoteFilepath).st_size:
                # If file exists and is the same size on remote pc, remove from list
                logger.warning(f'File: {filename[itr]} already exists on remote pc, skipping\n')
                filename.pop(itr)
                size.pop(itr)
                continue # Skip advancing itr
        itr += 1
    return [filename, size]

def pull_DataQ(hostname_DataQ, username_DataQ, password_DataQ, localPath, sourcePath_DataQ, 
               filename, size, logger):
    for i in range(0,len(filename)):
        localFilepath = os.path.join(localPath, filename[i])
        httpFilepath = os.path.join(sourcePath_DataQ, filename[i])
        print(f'Attempting to move: {httpFilepath} to: {localFilepath}')
        # Check if file already exists on local system
        if size[i] == 0:
            print(f'File: {httpFilepath} is empty (0 bytes), skipping')
            continue
        if os.path.isfile(localFilepath):
            if os.path.getsize(localFilepath) == size[i]:
                print(f'File: {localFilepath} already exists, skipping')
                continue # If file exists and is the same size continue loop
        # Pull http file
        get_HTTP_File(hostname_DataQ, httpFilepath, username_DataQ, password_DataQ, 
                      localFilepath)
        # Check if local file exists and is the same size as remote
        if os.path.isfile(localFilepath):
            if os.path.getsize(localFilepath) == size[i]:
                print('Successful Transfer of: ' + str(filename[i]) + '\n')
            else:
                raise ValueError('Failed Transfer of: ' + str(filename[i]) + '\n')
        else:
            raise ValueError('Failed Transfer of: ' + str(filename[i]) + '\n')

def push_DataQ(hostname_Transfer, username_Transfer, password_Transfer, localPath, localBackup,
                transferPath, logger):
    backupTime = time() - 24*60*60 * 60
    sftp_Local = None
    if password_Transfer:
        sftp_Transfer = sftp_Server_wPass(hostname_Transfer, username_Transfer, password_Transfer)
    else:
        sftp_Transfer = sftp_Server(hostname_Transfer, username_Transfer)
    folder2folder(localPath, sftp_Local, transferPath, sftp_Transfer, logger)
    backup_Folder(localPath, sftp_Local, localBackup, backupTime, logger)

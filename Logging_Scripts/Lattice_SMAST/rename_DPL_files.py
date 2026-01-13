# Rename all f_open error files with correct datetime stamp

import os
import glob
from datetime import datetime

def rename_DPL():
    localPath = '/home/pi/Data/Tower_SMAST/'
    srchKey = '*f_open*'
    ext = '.txt'
    for fileName in glob.glob(localPath + srchKey):
        with open(fileName, 'r') as f:
            dataLine = f.read(21)
            print(f'datetime found: {dataLine}')
            # Create title from DPL time
            timeStamp = dataLine[:17]
            timeStamp = timeStamp.replace(':','-')
            dataTitle = fileName[:(len(localPath)+22)]
            fixedFileName = dataTitle + timeStamp + ext
            fixedFileName = fixedFileName.replace(' ','')
            if os.path.isfile(fixedFileName):
                print(f'Duplicate File. Removing: {fileName}')
                os.system(f'rm {fileName}')
            else:
                print(f'Moving: {fileName}\nTo: {fixedFileName}')
                os.system(f'mv {fileName} {fixedFileName}')

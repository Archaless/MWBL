# Created by Tyler Knapp 2025-10-08
# Run this script to pull data from the AQMesh API
# Run in crontab with: 0 * * * * /usr/bin/python3 /usr2/MWBL/Data/AQMesh/Scripts/Pull_AQMesh.py

import AQMesh_Scripts as AQMS
printFlag = True # Set to True to enable printing
username = "TylerKnapp"
password = "4metdata@SMAST"
savePath = "/usr2/MWBL/Data/AQMesh/raw/" # ensure trailing '/' is included

AQMS.auth_request(username,password,printFlag)
AQMS.asset_request(printFlag)
AQMS.next_request(savePath,printFlag)
#AQMS.repeat_request(savePath,printFlag) # Helpful for testing, only pulls once
#AQMS.PF_request(printFlag) # Use to update Pod frequencies
#AQMS.SD_request(printFlag) # Use to pull sensor details
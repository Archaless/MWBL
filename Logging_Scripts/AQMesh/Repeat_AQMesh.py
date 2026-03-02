import AQMesh_Scripts as AQMS
printFlag = True # Set to True to enable printing
username = "TylerKnapp"
password = "4metdata@SMAST"
savePath = "/usr2/MWBL/Data/AQMesh/raw/" # ensure trailing '/' is included

AQMS.auth_request(username,password,printFlag)
AQMS.asset_request(printFlag)
# AND
AQMS.repeat_request(savePath,printFlag) # Helpful for testing, only pulls once
# And/OR
#AQMS.PF_request(printFlag) # Use to update Pod frequencies
# And/OR
#AQMS.SD_request(printFlag) # Use to pull sensor details
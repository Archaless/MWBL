#!/bin/bash
# NOTE: For future users:
#   Change "username" to your username
#   Ensure you are in the MWBL group on MWBL and the oms-admin group on the oms-smast server
#   & share your paired ssh key with the server (i.e. "ssh-copy-id *your username*@134.88.228.97")
#   Set this script to a cronjob on your user on MWBL
#   Done!

parentPath="/usr2/MWBL/Data"
username="tknapp"
hostname="134.88.228.97"

for folderPath in $parentPath/*/; do
    folderName=$(basename "$folderPath")
    if folderName == "Lattice_SMAST_Station1" || folderName == "Lattice_CBC_Station2" || folderName == "Misc_Data" || folderName == "NBAirport" || folderName == "EPA_PM25" || folderName == "NOAA_WaterT"; then
        continue
    fi
    folderPath_MWBL="$folderPath/processed/*"
    zipPath_MWBL="$folderPath/processed"
    logPath_MWBL="$folderPath/server_Transfer_Log.txt"
    folderPath_OMS="/data/$folderName/"
    zipPath_OMS="/data/Zip_Archives/$folderName.zip"
    # Copy processed data to OMS server
    rsync -avz --log-file="$logPath_MWBL" $folderPath_MWBL "$username@$hostname:$folderPath_OMS" # NOTE: $folderPath_MWBL must be a literal not a string
    scp "$logPath_MWBL" "$username@$hostname:$folderPath_OMS"
    # Create zip archive of processed folder and move to OMS server
    zip -r -q "$folderPath$folderName.zip" "$zipPath_MWBL"
    scp "$folderPath$folderName.zip" "$username@$hostname:$zipPath_OMS"
done

parentPath="/usr2/MWBL/Data/Lattice_SMAST_Station1"

for folderPath in $parentPath/*/; do # folderPath ex. /usr2/MWBL/Data/Lattice_SMAST_Station1/Gill
    folderName=$(basename "$folderPath") # folderName ex. Gill
    folderPath_MWBL="$folderPath/processed/*"
    zipPath_MWBL="$folderPath/processed"
    logPath_MWBL="$folderPath/server_Transfer_Log.txt"
    folderPath_OMS=/data/Lattice_SMAST_Station1/$folderName/
    zipPath_OMS="/data/Zip_Archives/Lattice_SMAST_Station1_$folderName.zip"
    # Copy processed data to OMS server
    rsync -avz --log-file="$logPath_MWBL" $folderPath_MWBL "$username@$hostname:$folderPath_OMS"
    scp "$logPath_MWBL" "$username@$hostname:$folderPath_OMS"
    # Create zip archive of processed folder and move to OMS server
    zip -r -q "$folderPath$folderName.zip" "$zipPath_MWBL"
    scp "$folderPath$folderName.zip" "$username@$hostname:$zipPath_OMS"
done

parentPath="/usr2/MWBL/Data/Lattice_CBC_Station2"

for folderPath in $parentPath/*/; do # folderPath ex. /usr2/MWBL/Data/Lattice_CBC_Station2/Gill
    folderName=$(basename "$folderPath") # folderName ex. Gill
    folderPath_MWBL="$folderPath/processed"
    zipPath_MWBL="$folderPath/processed"
    logPath_MWBL="$folderPath/server_Transfer_Log.txt"
    folderPath_OMS=/data/Lattice_CBC_Station2/$folderName/
    zipPath_OMS="/data/Zip_Archives/Lattice_CBC_Station2_$folderName.zip"
    # Copy processed data to OMS server
    rsync -avz --log-file="$logPath_MWBL" $folderPath_MWBL "$username@$hostname:$folderPath_OMS"
    scp "$logPath_MWBL" "$username@$hostname:$folderPath_OMS"
    # Create zip archive of processed folder and move to OMS server
    zip -r -q "$folderPath$folderName.zip" "$zipPath_MWBL"
    scp "$folderPath$folderName.zip" "$username@$hostname:$zipPath_OMS"
done
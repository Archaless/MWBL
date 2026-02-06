username="tknapp"
hostname="134.88.228.97"
# Sync latest condition images
path_MWBL="/usr2/MWBL/Analysis/latest_conditions/*.jpg"
path_OMS="/var/www/html/oms-smast/latest_conditions/"
datePath_MWBL="/usr2/MWBL/Analysis/latest_conditions/date.txt"
# Write current date/time to file
date +"%Y-%m-%d %H:%M:%S" > "$datePath_MWBL"
# Copy processed data to OMS server
scp $path_MWBL "$username@$hostname:$path_OMS" # NOTE: $path_MWBL must be a literal not a string
scp "$datePath_MWBL" "$username@$hostname:$path_OMS" # NOTE: $path_MWBL must be a literal not a string
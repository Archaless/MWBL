import os
from time import sleep
import paramiko

###########################################################################
                      ### Network Functions ###
###########################################################################

def connect2sys(hostname):
    maxAttempts = 3
    itr = 0
    while True:
        try:
            if ping_IP(hostname) == 0:
                break
            restart_Network(itr)
        except:
            pass
        if itr > maxAttempts: raise ConnectionError(f'ERROR: Unable to connect to {hostname}\n')
        itr += 1

def ping_IP(host):
    response = os.system(f'ping -c 1 {host} >/dev/null 2>&1') # Sucessful if 0 is returned
    return response

# Restart network adapter (LINUX ONLY)
def restart_Network(adapterNum):
    if adapterNum >= 0: # Nominally 0 or 1
         # Force ALL eth# to turn off
        for i in range(5):
            try:
                x = os.system(f'sudo ifconfig eth{i} down >/dev/null 2>&1')
            except:
                pass
        x = os.system(f'sudo ifconfig eth{adapterNum} up >/dev/null 2>&1') # Force eth# to turn on
    else: # Nominally -1 to restart wifi
        x = os.system('sudo ifconfig wlan0 down >/dev/null 2>&1') # Force wifi to turn off
        x = os.system('sudo ifconfig wlan0 up >/dev/null 2>&1') # Force wifi to turn on
    sleep(10) # Buffer period

# Create an SFTP client object
def sftp_Server(hostname, username, rsaPath='/home/pi/.ssh/id_rsa'):
    piKey = paramiko.RSAKey.from_private_key_file(rsaPath)
    sshClient = paramiko.SSHClient()
    sshClient.load_system_host_keys()
    sshClient.default_window_size = 2147483647 # Increase the ammount of data allowed to be transferred
    sshClient.default_max_packet_size = 32768
    sshClient.connect(hostname=hostname,username=username,allow_agent=True,pkey=piKey,timeout=60)
    sftp = sshClient.open_sftp()
    return sftp

# Create an SFTP client object
def sftp_Server_wPass(hostname, username, password):
    sshClient = paramiko.SSHClient()
    sshClient.load_system_host_keys()
    sshClient.default_window_size = 2147483647 # Increase the ammount of data allowed to be transferred
    sshClient.default_max_packet_size = 32768
    sshClient.connect(hostname=hostname,username=username,password=password,allow_agent=True,timeout=60)
    sftp = sshClient.open_sftp()
    return sftp

# Check if remote file exists
def sftp_IsFile(remoteFilepath, sftp):
    try:
        sftp.stat(remoteFilepath)
        isFile = True # If above didn't throw an error, file must exist
    except:
        isFile = False
    return isFile

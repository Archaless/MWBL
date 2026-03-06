import os
from serial.tools import list_ports
from serial import Serial

###########################################################################
                         ### Serial Functions ###
###########################################################################

def connect2serial(vid, pid, logger=None, baudRate=9600, bytesize=8, parity='N',\
                    stopbits=1, timeout=1):
    serialPath = find_Port(vid, pid)
    # Open serial connection to DPL
    if os.path.exists(serialPath):
        serialStream = Serial(serialPath, baudRate, bytesize, parity, stopbits,\
                                    timeout)
    else:
        raise ValueError('ERROR: Serial Path not found')
    if not logger == None:
        logger.info('SERIAL - connection open')
    return serialStream

def find_Port(vid, pid):
    usbPath = None
    for port in list_ports.comports():
        if port.vid == vid and port.pid == pid:
            usbPath = port.device
    if usbPath == None:
        raise NameError(f'USB Path for device: {vid}:{pid} not found')
    return usbPath

def restart_Serial(vid,pid):
    serialPath = find_Port(vid, pid)
    response = os.system(f'sudo usbreset {serialPath}')
    return response
import os
import sys
from serial import Serial, tools
from time import sleep

def find_Port(vid, pid):
	usbPath = None
	for port in tools.list_ports.comports():
		if port.vid == vid and port.pid == pid:
			usbPath = port.device
	if usbPath == None:
		raise NameError('USB Path for device: {vid}:{pid} not found')
	return usbPath

def connect_Serial(baud, vid, pid):
	usbPath = find_Port(vid, pid)
	try:
		ser = Serial(usbPath, baud)
	except:
		response = os.system(f'sudo usbreset {usbPath}')
		usbPath = find_Port(vid, pid)
		if response:
			sleep(1)
			ser = Serial(usbPath, baud)
		else:
			raise ValueError(f'Cannot restart device: {usbPath}')
	return ser

def test_Relay(baud, vid, pid):
	openRelay = 'A0 01 01 A2'
	closeRelay = 'A0 01 00 A1'
	with connect_Serial(baud, vid, pid) as ser:
		print('Opening!')
		ser.write(bytes.fromhex(openRelay))
		sleep(1)
		print('Closing!')
		ser.write(bytes.fromhex(closeRelay))
		sleep(1)

def main():
	baud = 9600
	vid = 0x1a86 # CH340 Chip (USB Relay)
	pid = 0x7523 # CH340 Chip (USB Relay)

	for i in range(0,3):
		test_Relay(baud, vid, pid)
	return 0

if __name__ == '__main__':
	sys.exit(main())
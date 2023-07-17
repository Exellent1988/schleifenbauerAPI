# -*- coding: utf-8 -*-
'''
Copyright:	Schleifenbauer - 2019
Version:	1.1.5
Authors:	Laurent - laurent.schuermans@schleifenbauer.eu
			Schleifenbauer - support@schleifenbauer.eu

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

This software is provided "as is" and Schleifenbauer disclaims all warranties
with regard to this software including all implied warranties of merchantability
and fitness. In no event shall Schleifenbauer be liable for any special, direct,
indirect, or consequential damages or any damages whatsoever resulting from loss
of use, data or profits, whether in an action of contract, negligence or other
tortious action, arising out of or in connection with the use or performance of
this software.
'''

import time

from hlapi.hlapi import HLAPI
from hlapi.DeviceManager import DeviceManager
from hlapi.managers.MultiReadWrite import MultiReadWrite

interfaces = {
	"192.168.9.100": {
		"webapi_port": 80,
		"webapi_user": "power",
		"webapi_pass": "power",
		"ipapi_key": "0000000000000000"
	}
}

# read some PDU alert values
mnemonics = ['ssstat', 'ssttri', 'ssitri', 'ssotri', 'ssvtri']

# method to print progress percentage
def showPercentage(progressManager):
	progressManager.waitForInit() # make sure the process has started
	last_percentage = 0
	print("0%")
	while progressManager.isRunning():
		percentage = progressManager.getStatus()[1]
		if percentage > last_percentage+10:
			print(str(percentage)+"%")
			last_percentage = percentage
		time.sleep(0.1)
	print("100%")
	progressManager.closeThreads() # make sure the process ends

hlapi = HLAPI(debug=False)

# scan databus, identify devices
deviceManager = DeviceManager(hlapi)
deviceManager.startLoadInterfaces(interfaces)
showPercentage(deviceManager.progress)

devices = deviceManager.devices
print(len(devices), "devices found")

# read registers from found devices
multiReadWrite = MultiReadWrite(hlapi, devices)
multiReadWrite.startReadAll(mnemonics)
showPercentage(multiReadWrite.progress)

# pretty-print result
for uid, output in multiReadWrite.result.items():
	print(uid)
	for mnemonic, value in output['data'].items():
		print("\t", mnemonic, value)

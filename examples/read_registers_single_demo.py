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

hlapi = HLAPI(debug=False)
# identify devices
deviceManager = DeviceManager(hlapi)
deviceManager.loadInterfaces(interfaces)
# read firmware version
multiReadWrite = MultiReadWrite(hlapi, deviceManager.devices)
firmwareVersions = multiReadWrite.readSingle('idfwvs')
# pretty-print result
for uid, output in firmwareVersions.items():
	print(uid, output['data'])

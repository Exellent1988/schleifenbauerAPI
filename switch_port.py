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
import sys

from hlapi.hlapi import HLAPI
from hlapi.DeviceManager import DeviceManager
from hlapi.managers.MultiReadWrite import MultiReadWrite

# interfaces = {
# 	"10.123.1.38": {
# 		"webapi_port": 80,
# 		"webapi_user": "power",
# 		"webapi_pass": "power",
# 		"ipapi_key": "0000000000000000"
# 	}
# }
ip = sys.argv[1]
port = int(sys.argv[2])
status = int(sys.argv[3])
interfaces = {
	ip: {
		"webapi_port": 80,
		"webapi_user": "power",
		"webapi_pass": "power",
		"ipapi_key": "0000000000000000"
	}
}

hlapi = HLAPI(debug=False)

# Identify interface
deviceManager = DeviceManager(hlapi)
deviceManager.loadInterfaces(interfaces)

# Use only first device
targetDevice = deviceManager.devices[0]
print("Found device:", targetDevice)

outlet_state = targetDevice.read('swocst', 'single', extract=True)
print("Current outlet state:", outlet_state)

# Safety measure
if outlet_state is None or len(outlet_state) != 54:
	sys.exit()

# Unlock all outlets
outlet_unlock = [1] * 54
print("Unlock success?", targetDevice.write('swounl', 'single', outlet_unlock))

outlet_state[port] = status

print("Switch success?", targetDevice.write('swocst', 'single', outlet_state))

# Wait 10 seconds for PDU to update internal outlet status
time.sleep(10)
print("New outlet state:", targetDevice.read('swocst', 'single', extract=True, cache=False))

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


# Standardwerte festlegen
default_ip = "10.10.20.173"
default_port = 80
default_user = "power"
default_password = "power"
default_apikey = "0000000000000000"
default_ports = "all"
default_device_id = 0
default_state = 1

if "--help" in sys.argv:
    print("Anleitung zur Verwendung:")
    print("- Argument 1: IP-Adresse")
    print("- Argument 2: WebAPI-Port | default = 80")
    print("- Argument 3: Benutzer| default = 'power'")
    print("- Argument 4: Passwort| default = 'power' ")
    print("- Argument 5: API-Schlüssel | default = '0000000000000000' ")
    print("- Argument 6: Target DeviceID | default = 0 ")
    print("- Argument 7: Zu Schlatender Port der PDU | default = 'all' (0-24) ")
    print("- Argument 8: Zustand den der Port erhalten soll | default = 'on' ('on','off','toggle')")
    sys.exit(0)
# Argumente verarbeiten oder Standardwerte verwenden
ip = sys.argv[1] if len(sys.argv) > 1 else default_ip
apiport = int(sys.argv[2]) if len(sys.argv) > 2 else default_port
user = sys.argv[3] if len(sys.argv) > 3 else default_user
password = sys.argv[4] if len(sys.argv) > 4 else default_password
apikey = sys.argv[5] if len(sys.argv) > 5 else default_apikey
device_id = int(sys.argv[6]) if len(sys.argv) > 6 else default_device_id
port = sys.argv[7] if len(sys.argv) > 7 else default_ports
state = sys.argv[8] if len(sys.argv) > 8 else default_state

interfaces = {
	ip: {
		"webapi_port": apiport,
		"webapi_user": user,
		"webapi_pass": password,
		"webapi_key": apikey
	}
}

hlapi = HLAPI(debug=False)

# Identify interface
deviceManager = DeviceManager(hlapi)
deviceManager.loadInterfaces(interfaces)

# Use only first device
targetDevice = deviceManager.devices[device_id]
print("Found device:", targetDevice)

outlet_state = targetDevice.read('swocst', 'single', extract=True)
print("Current outlet state:", outlet_state)

# Safety measure
if outlet_state is None or len(outlet_state) != 54:
	sys.exit()

# Unlock all outlets
outlet_unlock = [1] * 54
print("Unlock success?", targetDevice.write('swounl', 'single', outlet_unlock))
if port == 'all':
	for i in range(len(outlet_state)):
		if state  == 'on':
			state = 1
		elif state == 'off':
			state = 0
		elif state == 'toggle':
			state = outlet_state[i] ^ 1
			
		outlet_state[i] = state
	
else:
	if state  == 'on':
		state = 1
	elif state == 'off':
		state = 0
	elif state == 'toggle':
		state = outlet_state[port] ^ 1
	outlet_state[port] = state

print("Switch success?", targetDevice.write('swocst', 'single', outlet_state))

# Wait 10 seconds for PDU to update internal outlet status
time.sleep(10)
print("New outlet state:", targetDevice.read('swocst', 'single', extract=True, cache=False))

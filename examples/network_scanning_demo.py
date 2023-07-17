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
from hlapi.NetworkScanner import NetworkScanner
from hlapi.DeviceManager import DeviceManager

hlapi = HLAPI(debug=False)

subnet = "192.168.9.*" # * means scan from .0 to .255
http_port = 80
webapi_user = "power"

# Start scanning
networkScanner = NetworkScanner(hlapi, subnet, http_port, webapi_user)
networkScanner.startScan()

# Wait until scanner is done, more info on progress in section 4.4
while networkScanner.progress.isRunning():
	time.sleep(1)

# Print the result
print(networkScanner.result)

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
import argparse

from hlapi.hlapi import HLAPI
from hlapi.DeviceManager import DeviceManager


# Standardwerte festlegen
default_ip = "10.10.20.173"
default_port = 80
default_user = "power"
default_password = "power"
default_apikey = "0000000000000000"
default_ports = "all"
default_device_id = 0
default_state = 'on'


def parse_arguments():
    parser = argparse.ArgumentParser(description="Schaltsteuerung für PDU")
    parser.add_argument("--ip", default=default_ip, help="IP-Adresse")
    parser.add_argument("--apiport", type=int, default=default_port, help="WebAPI-Port")
    parser.add_argument("--user", default=default_user, help="Benutzer")
    parser.add_argument("--password", default=default_password, help="Passwort")
    parser.add_argument("--apikey", default=default_apikey, help="API-Schlüssel")
    parser.add_argument("--device_id", type=int, default=default_device_id, help="Target DeviceID")
    parser.add_argument("--port", default=default_ports, help="Zu schaltender Port der PDU")
    parser.add_argument("--state", default=default_state, help="Zustand, den der Port erhalten soll")

    return parser.parse_args()


def main():
    args = parse_arguments()
    interfaces = {
        args.ip: {
            "webapi_port": args.apiport,
            "webapi_user": args.user,
            "webapi_pass": args.password,
            "ipapi_key": args.apikey
        }
    }

    hlapi = HLAPI(debug=True)

    # Identify interface
    deviceManager = DeviceManager(hlapi)
    deviceManager.loadInterfaces(interfaces)

    # Use only first device
    targetDevice = deviceManager.devices[args.device_id]
    print("Found device:", targetDevice)

    outlet_state = targetDevice.read('swocst', 'single', extract=True)
    print("Current outlet state:", outlet_state)

    # Safety measure
    if outlet_state is None or len(outlet_state) != 54:
        sys.exit()

    # Unlock all outlets
    outlet_unlock = [1] * 54
    print("Unlock success?", targetDevice.write('swounl', 'single', outlet_unlock))

    if args.port == 'all':
        for i in range(len(outlet_state)):
            if args.state == 'on':
                state = 1
            elif args.state == 'off':
                state = 0
            elif args.state == 'toggle':
                state = outlet_state[i] ^ 1

            outlet_state[i] = state

    else:
        if args.state == 'on':
            state = 1
        elif args.state == 'off':
            state = 0
        elif args.state == 'toggle':
            state = outlet_state[int(args.port)] ^ 1
        outlet_state[int(args.port)] = state

    print("Switch success?", targetDevice.write('swocst', 'single', outlet_state))

    # Wait 10 seconds for PDU to update internal outlet status
    time.sleep(10)
    print("New outlet state:", targetDevice.read('swocst', 'single', extract=True, cache=False))


if __name__ == "__main__":
    main()

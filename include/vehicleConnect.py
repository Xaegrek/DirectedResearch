from include import globalVariables as gVar

from dronekit import *
from pymavlink import mavutil
import droneapi
# import gps

import socket
import time
import sys
import argparse
import sys

def ConnectToUAV(self):
	while self.uInputLaunch == "":
		time.sleep(1)
	print("Starting attempt at SOLO Connection")

	if gVar.GPS == False:
		print("disabling GPS requirement")
		gVar.UAVS.parameters['ARMING_CHECK'] = -9

	# simulation vehicle, does not work on ARM processors
	if self.uInputLaunch == "0":
		parser = argparse.ArgumentParser(
			description='Print out vehicle state information. Connects to SITL on local PC by default.')
		parser.add_argument('--connect',
							help="Vehicle connection target string. If not specified, SITL automatically started and used.")
		args = parser.parse_args()

		import dronekit_sitl
		sitl = dronekit_sitl.start_default()
		connection_string = sitl.connection_string()

		# connecting to sitl vehicle
		print("connecting to vehicle on %s") % connection_string
		gVar.UAVS = connect(connection_string, wait_ready=True)

	# live vehicle
	elif self.uInputLaunch == "1":
		parser = argparse.ArgumentParser(
			description='Print out vehicle state information. Connects to SITL on local PC by default.')
		parser.add_argument('--connect', default='57600', help="vehicle connection target. Default '57600'")  # 115200
		args = parser.parse_args()
		gVar.UAVS = connect('/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00', baud=57600,
							rate=6)  # this line may need to be changed, specifically the /dev to a specific place, the rate, or teh baud rate

	else:
		print("invalid option, try another input")

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


def takeOff():
	print("starting basic prearm check")
	print(gVar.UAVS.mode.name)

	if gVar.UAVS.mode.name == "INITIALISING":  # todo can this be done better
		print("waiting for initialisation")
		time.sleep(3)

	if gVar.GPS == True:
		while gVar.UAVS.gps_0.fix_type < 3:
			print(gVar.UAVS.gps_0.fix_type, "satellites, waiting for more")
			time.sleep(1)

	print("uav should be in 'guided' mode")  # todo does this need to be done?
	print("current mode is", gVar.UAVS.mode.name)
	time.sleep(3)

	if gVar.GPS == True:
		while not gVar.UAVS.is_armable:  #hangs if no gps
			print("waiting for uav to be armable")
			time.sleep(1)

	print("arming motors")
	time.sleep(0.5)
	gVar.UAVS.mode = VehicleMode("GUIDED")
	gVar.UAVS.armed = True
	gVar.UAVS.flush()

	i=0
	while not gVar.UAVS.armed:
		print("waiting for uav to change modes")
		print("curront mode is", gVar.UAVS.mode.name)
		print("uav is armed?:", gVar.UAVS.armed)
		time.sleep(1)
		if i > 10:
			sys.exit("Did not arm within 10 seconds, check UAV")
		i += 1

	print("taking off - stand clear: altitude", gVar.altitudeTarget)
	print("target altitutude", gVar.altitudeTarget)
	time.sleep(4)
	gVar.UAVS.simple_takeoff(gVar.altitudeTarget)
	gVar.UAVS.flush()


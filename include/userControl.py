# allows user input during running and selection and control of maneuvers
# may offload selection  to gui on off-board computer
# implementiatn of algorithms still on this side

from include import globalVariables as gVar
from include import vehicleConnect, vehicleTakeoff, vehicleMove, vehicleReturn
from pathing import simpleWaypoint

from dronekit import *
from pymavlink import mavutil
import droneapi
# import gps

import socket
import time
import sys
import argparse
import sys

from pathing import *

# begin running stuff
def userInput():
	while True:
		i = raw_input("enter 'takeoff' to Takeoff")
		if i == 'takeoff':
			break
	vehicleTakeoff.takeOff()
	# vehicleMove.vehicleStay()
	print("01. desired path 1 test-script: max area of ~10*15*15, from corner")
	print("02. desired path 1 test-script using curve interpolation: max area of ~10*15*15, from corner")
	print("03. pathing equation using randomly generated fields")
	gVar.launchCode = raw_input("Please enter the launch code for the desired script /n")
	if '01' == gVar.launchCode:
		simpleWaypoint.simpleWaypoint(gVar.desiredPath1)
	elif '02' == gVar.launchCode:
		simpleWaypoint.simpleArcWaypoint(gVar.desiredPath1)
	elif '03' == gVar.launchCode:
		print('still working on this')
	else:
		return
	raw_input("press Enter to Land")
	vehicleReturn.vehicleLand()

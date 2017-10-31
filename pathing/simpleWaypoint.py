from include import globalVariables as gVar
from include import vehicleMove

from dronekit import *
from pymavlink import mavutil
import droneapi
# import gps

import socket
import time
import sys
import argparse
import sys
from numpy import interp as intp

def commandList():
	# full list of coordiantes
	gVar.coordinatesGPS = gVar.UAVS.locations.global_relative_frame
	gVar.coordinatesRel = gVar.UAVS.locations.local_frame
	# altitude from strat
	gVar.coordinatesGPSalt = gVar.UAVS.locations.global_relative_frame.alt
	gVar.coordinatesRelalt = gVar.UAVS.locations.local_frame.down
	# north from start and latitude
	gVar.coordinatesGPSx = gVar.UAVS.locations.global_relative_frame.lat
	gVar.coordinatesRelx = gVar.UAVS.locations.local_frame.north
	# east from start and longitude
	gVar.coordinatesGPSx = gVar.UAVS.locations.global_relative_frame.lon
	gVar.coordinatesRelx = gVar.UAVS.locations.local_frame.east
	#attitude
	gVar.attitude = gVar.UAVS.Attitude
	gVar.attitudePitch = gVar.UAVS.Attitude.pitch
	gVar.attitudeRoll = gVar.UAVS.Attitude.roll
	gVar.attitudeYaw = gVar.UAVS.Attitude.yaw

def simpleWaypoint(path):
	# takes:
	# 	current gps position
	# goal:
	# 	poth between set of GPS coordinates
	gVar.coordinatesGPS = gVar.UAVS.locations.global_relative_frame
	gVar.coordinatesRel = gVar.UAVS.locations.local_frame
	for i in range(len(path)):
		vehicleMove.vehicleMoveDistancet(path[i], gVar.uSpeed)

def simpleArcWaypoint(pathPTS):	#todo rewrite this to use vehicleMove and a second one to try using interpolation
	# takes:
	# 	current gps position
	# goal:
	# 	path and iterplotae set of GPS cooridanets
	gVar.coordinatesGPS = gVar.UAVS.locations.global_relative_frame
	gVar.coordinatesRel = gVar.UAVS.locations.local_frame
	for i in range(len(pathPTS)):
		vehicleMove.vehicleMoveDistancet(pathPTS[i], gVar.uSpeed)

def simpleRiskPath():
	# takes:
	# 	gps position
	# 	coordinate risk map
	# goal:
	# 	path through heatmap using cost control analysis
	# 	likely use path interpolation
	gVar.coordinatesGPS = gVar.UAVS.locations.global_relative_frame
	gVar.coordinatesRel = gVar.UAVS.locations.local_frame

# Flight path to run
# not being used
def run():
	gVar.UAVS.airspeed = 0.5  # m/s
	# simpleWaypoint(gVar.desiredPath1)
	simpleArcWaypoint(gVar.desiredPath1)


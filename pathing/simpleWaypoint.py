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
	for i in len(path):
		gVar.UAVS.simple_goto(path[i])
		while gVar.UAVS.locations.local_frame != path[i]:
			time.sleep(1)
			print(gVar.UAVS.locations.local_frame)

def simpleArcWaypoint():
	# takes:
	# 	current gps position
	# goal:
	# 	path and iterplotae set of GPS cooridanets
	gVar.coordinatesGPS = gVar.UAVS.locations.global_relative_frame
	gVar.coordinatesRel = gVar.UAVS.locations.local_frame
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
def run():
	gVar.UAVS.airspeed = 0.5  # m/s
	simpleWaypoint(gVar.desiredPath1)
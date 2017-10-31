from include import globalVariables as gVar

from numpy import interp as intp
from numpy import linspace

from dronekit import *
from pymavlink import mavutil
import droneapi
# import gps

import socket
import time
import sys
import argparse
import sys


def vehicleStay():
	time.sleep(gVar.flyTime)

def vehicleMoveVelocity():
	return

def vehicleMoveDistancet(pp, speed): #time based run
	pathPoint = LocationGlobalRelative(pp[0],pp[1],pp[2]) #todo or make this LocationLocal(dn,de,-dz)
	gVar.UAVS.simple_goto(pathPoint,speed)
	u=time.time()
	un = u+5
	while u< un:
		gVar.posHistory.append([gVar.UAVS.location.local_frame])
		print(gVar.UAVS.location.global_relative_frame)
		time.sleep(0.2)
		u=time.time()
	return

def vehicleMoveDistanced(pp,speed):
	currentLocation = gVar.UAVS.location.global_relative_frame
	targetLocation = get_location_metres(currentLocation, pp[0], pp[1])
	targetDistance = get_distance_metres(currentLocation, targetLocation)

	gVar.UAVS.simple_goto(targetLocation,speed)

	while gVar.UAVS.mode.name == "GUIDED":  # Stop action if we are no longer in guided mode.
		remainingDistance = get_distance_metres(gVar.UAVS.location.global_relative_frame, targetLocation)
		print("Distance to target: ", remainingDistance)
		gVar.posHistory.append([gVar.UAVS.location.local_frame])
		if remainingDistance <= targetDistance * 0.01:  # Just below target, in case of undershoot.
			print("Reached target")
			break
		time.sleep(1)

def simpleArcInterpolater(path):
	# takes:
	# 	current gps position
	# goal:
	# 	path and iterplotae set of GPS cooridanets
	num_true_pts = 50
	pathD = [[],[],[]]
	smoothPath = []
	for i in range(len(path)):
		pathD[0].append(path[i][0])
		pathD[1].append(path[i][1])
		pathD[2].append(path[i][2])
	tck, u = intp.splprep(pathD)
	u_fine = linspace(0, 1, num_true_pts)
	x_fine, y_fine, z_fine = intp.splev(u_fine, tck)
	for i in range(len(x_fine)):
		smoothPath.append([x_fine[i], y_fine[i], z_fine[i]])
	return smoothPath

def pathFollow(path):
	gVar.coordinatesGPS = gVar.UAVS.location.global_relative_frame
	gVar.coordinatesRel = gVar.UAVS.location.local_frame
	for i in range(len(path)):
		vehicleMoveDistancet(path[i], gVar.uSpeed)
	return

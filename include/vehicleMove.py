from include import globalVariables as gVar

from numpy import interp as intp
from numpy import linspace
import numpy as sp

from dronekit import *
from pymavlink import mavutil
import droneapi
# import gps

import socket
import time
import sys
import argparse
import sys

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

def vehicleStay():
	time.sleep(gVar.flyTime)

def vehicleMoveVelocity():
	return

###########################################

def vehicleMoveDistancet(pp, speed): #time based run
	pathPoint = LocationGlobalRelative(pp[0],pp[1],pp[2]) #todo or make this LocationLocal(dn,de,-dz)
	gVar.UAVS.simple_goto(pathPoint,speed)
	gVar.UAVS.flush()
	u=time.time()
	un = u+5
	print(gVar.UAVS.location.local_frame)
	while u< un:
		gVar.posHistory.append([gVar.UAVS.location.local_frame])
		print(gVar.UAVS.location.global_relative_frame)
		time.sleep(0.2)
		u=time.time()
	return

def get_location_metres(original_location, dNorth, dEast, dalt):
	earth_radius = 6378137.0  # Radius of "spherical" earth
	# Coordinate offsets in radians
	dLat = dNorth / earth_radius
	dLon = dEast / (earth_radius * sp.cos(sp.pi * original_location.lat / 180))

	# New position in decimal degrees
	newlat = original_location.lat + (dLat * 180 / sp.pi)
	newlon = original_location.lon + (dLon * 180 / sp.pi)
	if type(original_location) is LocationGlobal:
		targetlocation = LocationGlobal(newlat, newlon, dalt)
	elif type(original_location) is LocationGlobalRelative:
		targetlocation = LocationGlobalRelative(newlat, newlon, dalt)
	else:
		raise Exception("Invalid Location object passed")
	return targetlocation

def get_distance_metres(aLocation1, aLocation2):
	dlat = aLocation2.lat - aLocation1.lat
	dlong = aLocation2.lon - aLocation1.lon
	return sp.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5

def vehicleMoveDistanced(pp,speed):
	currentLocation = gVar.UAVS.location.global_relative_frame
	targetLocation = get_location_metres(currentLocation, pp[0], pp[1],pp[2])
	targetDistance = get_distance_metres(currentLocation, targetLocation)

	gVar.UAVS.simple_goto(targetLocation,speed)
	gVar.UAVS.flush()

	print('targetLocation:', targetLocation, 'currentLocation', currentLocation)
	while gVar.UAVS.mode.name == "GUIDED":  # Stop action if we are no longer in guided mode.
		remainingDistance = get_distance_metres(gVar.UAVS.location.global_relative_frame, targetLocation)
		print("Distance to target: ", remainingDistance)
		gVar.posHistory.append([gVar.UAVS.location.local_frame])
		gVar.poshistoryGPS.append([gVar.UAVS.location.global_relative_frame])
		if remainingDistance <= targetDistance * 0.01:  # Just below target, in case of undershoot.
			print("Reached target")
			break
		time.sleep(0.5)

def getDistance3D(aLocation1,aLocation2):

	return

def vehicleMoveDistanceMav(pp,speed):
	currentLocation = gVar.UAVS.location.global_relative_frame
	targetLocation = get_location_metres(currentLocation, pp[0], pp[1],pp[2])
	targetDistance = get_distance_metres(currentLocation, targetLocation)

	north = pp[0]; east = pp[1]; down = -pp[2]
	msg = gVar.UAVS.message_factory.set_position_target_local_ned_encode(
		0,  # time_boot_ms (not used)
		0, 0,  # target system, target component
		mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
		0b0000111111111000,  # type_mask (only positions enabled)
		north, east, down,  # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
		0, 0, 0,  # x, y, z velocity in m/s  (not used)
		0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
		0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
	# send command to vehicle
	gVar.UAVS.send_mavlink(msg)
	gVar.UAVS.flush()

	while gVar.UAVS.mode.name == "GUIDED":  # Stop action if we are no longer in guided mode.
		remainingDistance = get_distance_metres(gVar.UAVS.location.global_relative_frame, targetLocation)
		print("Distance to target: ", remainingDistance)
		gVar.posHistory.append([gVar.UAVS.location.local_frame])
		gVar.poshistoryGPS.append([gVar.UAVS.location.global_relative_frame])
		if remainingDistance <= targetDistance * 0.01:  # Just below target, in case of undershoot.
			print("Reached target")
			break
		time.sleep(0.5)

########################

def pathFollowt(path):	#time
	gVar.coordinatesGPS = gVar.UAVS.location.global_relative_frame
	gVar.coordinatesRel = gVar.UAVS.location.local_frame
	for i in range(len(path)):
		vehicleMoveDistancet(path[i], gVar.uSpeed)
	return

def pathFollowd(path): #distance
	gVar.coordinatesGPS = gVar.UAVS.location.global_relative_frame
	gVar.coordinatesRel = gVar.UAVS.location.local_frame
	for i in range(len(path)):
		vehicleMoveDistanced(path[i], gVar.uSpeed)
	return

def pathFollowMav(path): #mavlink
	gVar.coordinatesGPS = gVar.UAVS.location.global_relative_frame
	gVar.coordinatesRel = gVar.UAVS.location.local_frame
	for i in range(len(path)):
		vehicleMoveDistanceMav(path[i], gVar.uSpeed)
	return
# allows user input during running and selection and control of maneuvers
# may offload selection  to gui on off-board computer
# implementiatn of algorithms still on this side
# todo set up flight logging
from include import globalVariables as gVar
from include import vehicleConnect, vehicleTakeoff, vehicleMove, vehicleReturn
from pathing import simpleWaypoint
from pathing import djikstraThreatField_min as dj

from dronekit import *
from pymavlink import mavutil
import droneapi
# import gps

import socket
import time
import sys
import argparse
import sys
from datetime import datetime

from pathing import *

def skyBoxScale():
	# in the future, this can be removed from proper pathing, or used to as a border guard
	gVar.skyBox = [10,25,-5,15,-5,15]
	print("Current skybox, this will scale any path that goes over the margins:")
	print("zmin is %s m; zmax is %s m") % (gVar.skyBox[0], gVar.skyBox[1])
	print("north min is %s m, north max is %s m") % (gVar.skyBox[2], gVar.skyBox[3])
	print("east min is %s m, east max is %s m") % (gVar.skyBox[4], gVar.skyBox[5])
	check = raw_input("To change these values, enter 'modify': ")
	x = []
	if check == 'modify':
		x[0] = raw_input("new zmin value: ")
		x[1] = raw_input("new zmax value: ")
		x[2] = raw_input("new north min value: ")
		x[3] = raw_input("new north max value: ")
		x[4] = raw_input("new east min value: ")
		x[5] = raw_input("new east max value: ")
		for i in range(len(x)):
			if x[i]:
				gVar.skyBox[i] = x[i]
		print("Current skybox, this will scale any path that goes over the margins:")
		print("zmin is %s m; zmax is %s m") % (gVar.skyBox[0], gVar.skyBox[1])
		print("north min is %s m, north max is %s m") % (gVar.skyBox[2], gVar.skyBox[3])
		print("east min is %s m, east max is %s m") % (gVar.skyBox[4], gVar.skyBox[5])

	return

def scalePath(path):	#todo this, right now i'll just have it fail on a bad shape

	c = None
	nb = 0
	nt = 0
	eb = 0
	et = 0
	zb = 0
	zt = 0

	for i in range(len(path)):
		if path[i,0] < gVar.skyBox[2] and path[i,0] != abs(path[i,0]):
			gVar.kill = True
		elif path[i,0] > gVar.skyBox[3] and nt < abs(float(gVar.skyBox[3])/float(path[i,0])) :
			nt = abs(float(gVar.skyBox[3])/float(path[i,0]))
		elif path[i,1] < gVar.skyBox[4] and eb < abs(float(gVar.skyBox[4])/float(path[i,0])):
			eb = abs(float(gVar.skyBox[4])/float(path[i,0]))
		elif path[i,1] > gVar.skyBox[5] and et < abs(float(gVar.skyBox[5])/float(path[i,0])):
			et = abs(float(gVar.skyBox[5])/float(path[i,0]))
		try:
			if path[i, 3] < gVar.skyBox[0] and zb < abs(float(gVar.skyBox[0]) / float(path[i, 0])):
				zb = abs(float(gVar.skyBox[0]) / float(path[i, 0]))
		except:
			pass
		try:
			if path[i, 3] > gVar.skyBox[1] and zt < abs(float(gVar.skyBox[1]) / float(path[i, 0])):
				zt = abs(float(gVar.skyBox[1]) / float(path[i, 0]))
		except:
			pass

	for i in range(len(path)):
		path[i,0] = path[i,0] * c

	return

# begin running stuff
def userInput():
	skyBoxScale()
	print("current launch altitude set to %s m") % gVar.altitudeTarget
	ua = raw_input("if you would like to change this, type 'yes': ")
	if ua == 'yes':
		gVar.altitudeTarget = int(raw_input("what would you like the new altitude to be?: "))
		print(gVar.altitudeTarget)
	ua = None
	ua = raw_input("Type 'yes' to disable GPS requirement: ")
	if ua == 'yes':
		gVar.GPS = False
		print("GPS Disablede, \nbe cautious of flight\n\n\n")

	print("00. flies up to desired altitude, then immedietly lands")
	print("01. desired path 1 test-script: max area of ~10*15*15, from corner")
	print("02. desired path 1 test-script using curve interpolation: max area of ~10*15*15, from corner")
	print("03. pathing equation using randomly generated fields")
	gVar.launchCode = raw_input("Please enter the launch code for the desired script: \n")
	if '03' == gVar.launchCode:
		gVar.N_G = int(raw_input("How large should the grid be, basicall in metres: "))
		print("planning path")
		tempP= dj.coorDjik(gVar.N_G)
		for i in range(len(tempP)):
			gVar.desiredPathDJ = tempP.append(gVar.altitudeTarget)[i]
	elif '02' == gVar.launchCode:
		gVar.tdesiredPath = vehicleMove.simpleArcInterpolater(gVar.desiredPath1)

	#scale path if out of bounds
	if	gVar.launchCode == '01':
		desiredPath =gVar.desiredPath1
		#scalePath(desiredPath)
	elif gVar.launchCode == '02':
		desiredPath =gVar.tdesiredPath
		#scalePath(desiredPath)
	elif gVar.launchCode == '03':
		desiredPath =gVar.desiredPathDJ
		#scalePath(desiredPath)
	else:
		desiredPath = [0,0,gVar.altitudeTarget]

	if gVar.kill != False:
		sys.exit()

	#Flight begins
	while True:
		i = raw_input("enter 'takeoff' to Takeoff: ")
		if i == 'takeoff' and gVar.kill == False:
			break
	vehicleTakeoff.takeOff()
	print(gVar.UAVS.location.local_frame)
	print(gVar.UAVS.location.global_relative_frame)

	if '01' == gVar.launchCode:
		vehicleMove.pathFollow(desiredPath)
	elif '02' == gVar.launchCode:
		vehicleMove.pathFollow(desiredPath)
	elif '03' == gVar.launchCode:
		vehicleMove.pathFollow(desiredPath)
	elif '00' == gVar.launchCode:
		print("up and down as an intro case")
		time.sleep(25)
	else:
		return

	#might comment this out for test, will see
	# raw_input("press Enter to Land")
	vehicleReturn.vehicleLand()

	a= str(time.time())+'.txt'
	f = open(a,'a')
	f.write('desired path')
	f.write(str(desiredPath))
	f.write('actual path')
	f.write(str(gVar.posHistory))
	f.close()

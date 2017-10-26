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
from scipy import interpolate as intp
import random

def randomPather(area,rSeed):
	# create a random grid of either distances which need to minimize travel to some point
	# or random heat map/threat field to navigate.
	# 2d for simplicity
	# path should array of [x,y] points
	# after array is found, should pass it to vehicleMove for each point
	# likely will use djikstras


	path = gVar.optimTrajectory
	gVar.coordinatesRel = gVar.UAVS.locations.local_frame
	for i in range(len(path)):
		vehicleMove.vehicleMoveDistance(path[i],gVar.uSpeed)
	return
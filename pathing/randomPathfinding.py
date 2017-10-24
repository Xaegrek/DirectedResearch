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



	path = gVar.optimTrajectory
	gVar.coordinatesRel = gVar.UAVS.locations.local_frame
	for i in range(len(path)):
		vehicleMove.vehicleMoveDistance(path[i],gVar.uSpeed)
	return
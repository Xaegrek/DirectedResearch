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

def vehicleLand():
	print("\nbeginning landing sequence \n")
	self.UAVS.mode = VehicleMode("LAND")
	self.UAVS.close()
	self.UAVS.flush()

def vehicleHome():
	if gVar.GPS == True:
		print("\nReturning Home \n")
		self.UAVS.mode = VehicleMode("RTL")
		self.UAVS.close()
		self.UAVS.flush()

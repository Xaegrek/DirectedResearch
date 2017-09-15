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
	gVar.UAVS.mode = VehicleMode("LAND")
	gVar.UAVS.close()
	gVar.UAVS.flush()

def vehicleHome():
	if gVar.GPS == True:
		print("\nReturning Home \n")
		gVar.UAVS.mode = VehicleMode("RTL")
		gVar.UAVS.close()
		gVar.UAVS.flush()

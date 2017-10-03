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

def simpleWaypoint():
	takes:
		current gps position
	goal:
		poth between set of GPS coordinates
def simpleArcWaypoint():
	takes:
		current gps position
	goal:
		path and iterplotae set of GPS cooridanets
def simpleRiskPath
	takes:
		gps position
		coordinate risk map
	goal:
		path through heatmap using cost control analysis
		likely use path interpolation
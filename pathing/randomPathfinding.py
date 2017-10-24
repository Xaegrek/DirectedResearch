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
	
	return
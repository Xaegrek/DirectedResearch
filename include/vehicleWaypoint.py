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

def vehicleGoToWaypoint():
	return
# allows user input during running and selection and control of maneuvers
# may offload selection  to gui on off-board computer
# implementiatn of algorithms still on this side

from include import globalVariables as gVar
from include import vehicleConnect, vehicleTakeoff

from dronekit import *
from pymavlink import mavutil
import droneapi
# import gps

import socket
import time
import sys
import argparse
import sys

from pathing import *

# begin running stuff
def userInput():
	raw_input("press Enter to conitue")
	vehicleTakeoff.takeOff()
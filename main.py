from include import userControl
from include import vehicleConnect
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

class Main:
	def __init__(self, uInput, aAltitudeTarget, aFlyTime, gps):
		gVar.inputLaunch = uInput
		gVar.altitudeTarget = aAltitudeTarget
		gVar.flyTime = aFlyTime
		gVar.GPS = gps
		attempts = 0
		totalAttempts = 3
		while attempts < totalAttempts:
			try:
				vehicleConnect.connectToUAV()
				break
			except:
				attempts +=1
				print("Connection attempt #%s Failed, trying for %s total times.") % (attempts, totalAttempts)
				time.sleep(0.5)

	def run(self):
		userControl.userInput()
		return

# may want to rework how this works, though initilizing parameters could just be modified before full runtime
parser = argparse.ArgumentParser()
parser.add_argument("-input", dest='uInput', type=str, help="whether to run simulated or real uav, 0 or 1", default="1")
parser.add_argument("-AT", dest='aAltitudeTarget', type=int, help="how high to fly, in meters", default=10)
parser.add_argument("-FT", dest='aFlyTime', type=int, help="how long to fly, in seconds", default=10)
parser.add_argument("-GPS", dest='gps', type=bool, help="Default True, False disables GPS check during startup", default=True)
args = parser.parse_args()
main = Main(args.uInput, args.aAltitudeTarget, args.aFlyTime, args.gps)

try:
	main.run()
except KeyboardInterrupt:
	sys.exit()
from include import globalVariables as gVar

import dronekit
import socket
import exceptions
from pymavlink import mavutil
import droneapi
# import gps

import socket
import time
import sys
import argparse
import sys

def connectToUAV(pixhawkID):
	while gVar.inputLaunch == "":
		time.sleep(1)
	print("Starting attempt at SOLO Connection")

	# simulation vehicle, does not work on ARM processors
	if gVar.inputLaunch == "0":
		parser = argparse.ArgumentParser(
			description='Print out vehicle state information. Connects to SITL on local PC by default.')
		parser.add_argument('--connect',
							help="Vehicle connection target string. If not specified, SITL automatically started and used.")
		args = parser.parse_args()

		import dronekit_sitl
		sitl = dronekit_sitl.start_default()
		connection_string = sitl.connection_string()

		# connecting to sitl vehicle
		print("connecting to vehicle on %s") % connection_string
		gVar.UAVS = dronekit.connect(connection_string, wait_ready=True)

	# live vehicle, issues may come from plugging directly into pixhawk2
	elif gVar.inputLaunch == "1":
		try:
			gVar.UAVS = dronekit.connect(pixhawkID, rate=6,baud=115200, heartbeat_timeout=15 ,wait_ready = True)

		# Bad TCP connection
		except socket.error:
			print('No server exists!')

		# Bad TTY connection
		except exceptions.OSError as e:
			print('No serial exists!')

		# API Error
		except dronekit.APIException:
			print('Timeout!')

	else:
		print("invalid option, try another input")

	if gVar.GPS == False:
		print("disabling GPS requirement")
		gVar.UAVS.parameters['ARMING_CHECK'] = -9

def vehicleData():
	gVar.UAVS.wait_ready('autopilot_version')

	# Get all vehicle attributes (state)
	print("\nGet all vehicle attribute values:")
	print(" Autopilot Firmware version: %s") % gVar.UAVS.version
	print("   Major version number: %s") % gVar.UAVS.version.major
	print("   Minor version number: %s") % gVar.UAVS.version.minor
	print("   Patch version number: %s") % gVar.UAVS.version.patch
	print("   Release type: %s") % gVar.UAVS.version.release_type()
	print("   Release version: %s") % gVar.UAVS.version.release_version()
	print("   Stable release?: %s") % gVar.UAVS.version.is_stable()
	print(" Autopilot capabilities")
	print("   Supports MISSION_FLOAT message type: %s") % gVar.UAVS.capabilities.mission_float
	print("   Supports PARAM_FLOAT message type: %s") % gVar.UAVS.capabilities.param_float
	print("   Supports MISSION_INT message type: %s") % gVar.UAVS.capabilities.mission_int
	print("   Supports COMMAND_INT message type: %s") % gVar.UAVS.capabilities.command_int
	print("   Supports PARAM_UNION message type: %s") % gVar.UAVS.capabilities.param_union
	print("   Supports ftp for file transfers: %s") % gVar.UAVS.capabilities.ftp
	print("   Supports commanding attitude offboard: %s") % gVar.UAVS.capabilities.set_attitude_target
	print("   Supports commanding position and velocity targets in local NED frame: %s") % gVar.UAVS.capabilities.set_attitude_target_local_ned
	print("   Supports set position + velocity targets in global scaled integers: %s") % gVar.UAVS.capabilities.set_altitude_target_global_int
	print("   Supports terrain protocol / data handling: %s") % gVar.UAVS.capabilities.terrain
	print("   Supports direct actuator control: %s") % gVar.UAVS.capabilities.set_actuator_target
	print("   Supports the flight termination command: %s") % gVar.UAVS.capabilities.flight_termination
	print("   Supports mission_float message type: %s") % gVar.UAVS.capabilities.mission_float
	print("   Supports onboard compass calibration: %s") % gVar.UAVS.capabilities.compass_calibration
	print(" Global Location: %s") % gVar.UAVS.location.global_frame
	print(" Global Location (relative altitude): %s") % gVar.UAVS.location.global_relative_frame
	print(" Local Location: %s") % gVar.UAVS.location.local_frame
	print(" Attitude: %s") % gVar.UAVS.attitude
	print(" Velocity: %s") % gVar.UAVS.velocity
	print(" GPS: %s") % gVar.UAVS.gps_0
	print(" Gimbal status: %s") % gVar.UAVS.gimbal
	print(" Battery: %s") % gVar.UAVS.battery
	print(" EKF OK?: %s") % gVar.UAVS.ekf_ok
	print(" Last Heartbeat: %s") % gVar.UAVS.last_heartbeat
	print(" Rangefinder: %s") % gVar.UAVS.rangefinder
	print(" Rangefinder distance: %s") % gVar.UAVS.rangefinder.distance
	print(" Rangefinder voltage: %s") % gVar.UAVS.rangefinder.voltage
	print(" Heading: %s") % gVar.UAVS.heading
	print(" Is Armable?: %s") % gVar.UAVS.is_armable
	print(" System status: %s") % gVar.UAVS.system_status.state
	print(" Groundspeed: %s") % gVar.UAVS.groundspeed    # settable
	print(" Airspeed: %s") % gVar.UAVS.airspeed    # settable
	print(" Mode: %s") % gVar.UAVS.mode.name    # settable
	print(" Armed: %s") % gVar.UAVS.armed    # settable

def infoGPS():
	gVar.infoGPS = gVar.UAVS.GPSInfo


from dronekit import *
import droneapi
# import gps
import socket
import time
import sys
from pymavlink import mavutil
import argparse

import Global_Var as gbvar

def ConnectToUAV(SimvReal):
  while gbvar.uInputLaunch == "":
    time.sleep(1)
  print("Starting attempt at SOLO Connection")
  
  if gbvar.uInputLaunch =="0":
    parser = argparse.ArgumentParser(
      description='Print out vehicle state information. Connects to SITL on local PC by default.')
    parser.add_argument('--connect',
      help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    args = parser.parse_args()
    
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()
    
    #connecting to sitl vehicle
    print("connecting to vehicle on %s") % connection_string
    gbvar.UAVS = connect(connection_string, wait_ready = True)
    
  elif gbvar.uInputLaunch == "1":
    parser = argparse.ArgumentParser(
      description='Print out vehicle state information. Connects to SITL on local PC by default.')
    parser.add_argument('--connect', default='115200', help="vehicle connection target. Default '57600'")
    args = parser.parse_args()
    gbvar.UAVS = connect('/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00', baud=115200, rate=6)  #this line may need to be changed, specifically the /dev to a specific place, the rate, or teh baud rate
  
  else:
    print("invalid option")
    
def TakeOff(aAltitudeTarget, aFlyTime):
  print("starting basic prearm check")
  print(gbvar.UAVS.mode.name)
  
  if gbvar.UAVS.modeiname == "INITIALISING":  #todo can this be done better
    print("waiting for initialisation")
    time.sleep(1)
  while gbvar.UAVS.gps_0.fix_type < 3:
    print(gbvar.UAVS.gps_0.fix_type, "satellites, waiting for more")
    time.sleep(1)
  print("setting uav to guided mode")  #todo does this need to be done?
  print("current mode is", gbavr.UAVS.mode.name)
  time.sleep(1)
  
  while not gbvar.UAVS.is_armable:  #todo can i make this attempt arm after x tries?
    print("waiting for uav to be armable")
    time.sleep(1)
  
  print("arming motors")
  time.sleep(0.5)
  gbvar.UAVS.mode = VehicleMode("GUIDED")
  gbvar.UAVS.armed = True
  gbvar.UAVS.flush()
  
  while not gbvar.UAVS.armed: #todo should this attempt above steps after x tries?
    print("waiting for uav to change modes")
    print("curront mode is", gbvar.UAVS.mode.name
    timep.sleep(1)
    print("uav is armed?:", gbvar.UAVS.armed)
  
  print("taking off - stand clear")
  time.sleep(4)
  gbvar.UAVS.simple_takeoff(aAltitudeTarget)
  gbvar.UAVS.flush()
  time.sleep(aFlytime)
  
  gbvar.UAVS.mode = VehicleMode("LAND")
  gbvar.UAVS.close()
  gbvar.UAVS.flush()
    

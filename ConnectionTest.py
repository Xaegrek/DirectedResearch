from dronekit import *
import droneapi
# import gps
import socket
import time
import sys
from pymavlink import mavutil
import argparse
import sys

class Main:
  def __init__(self, uInput,aAltitudeTarget, aFlyTime):
    self.uInputLaunch = uInput
    self.aAltitudeTarget = aAltitudeTarget
    self.aFlyTime = aFlyTime
    self.UAVS = ""
    
  def ConnectToUAV(self):
    while self.uInputLaunch == "":
      time.sleep(1)
    print("Starting attempt at SOLO Connection")

    if self.uInputLaunch =="0":
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
      self.UAVS = connect(connection_string, wait_ready = True)

    elif self.uInputLaunch == "1":
      parser = argparse.ArgumentParser(
        description='Print out vehicle state information. Connects to SITL on local PC by default.')
      parser.add_argument('--connect', default='115200', help="vehicle connection target. Default '57600'")
      args = parser.parse_args()
      self.UAVS = connect('/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00', baud=115200, rate=6)  #this line may need to be changed, specifically the /dev to a specific place, the rate, or teh baud rate

    else:
      print("invalid option")

  def TakeOff(self):
    print("starting basic prearm check")
    print(self.UAVS.mode.name)

    if self.UAVS.modeiname == "INITIALISING":  #todo can this be done better
      print("waiting for initialisation")
      time.sleep(1)
    while self.UAVS.gps_0.fix_type < 3:
      print(self.UAVS.gps_0.fix_type, "satellites, waiting for more")
      time.sleep(1)
    print("setting uav to guided mode")  #todo does this need to be done?
    print("current mode is", gbavr.UAVS.mode.name)
    time.sleep(1)

    while not self.UAVS.is_armable:  #todo can i make this attempt arm after x tries?
      print("waiting for uav to be armable")
      time.sleep(1)

    print("arming motors")
    time.sleep(0.5)
    self.UAVS.mode = VehicleMode("GUIDED")
    self.UAVS.armed = True
    self.UAVS.flush()

    while not self.UAVS.armed: #todo should this attempt above steps after x tries?
      print("waiting for uav to change modes")
      print("curront mode is", self.UAVS.mode.name)
      time.sleep(1)
      print("uav is armed?:", self.UAVS.armed)

    print("taking off - stand clear")
    time.sleep(4)
    self.UAVS.simple_takeoff(aAltitudeTarget)
    self.UAVS.flush()
    time.sleep(aFlytime)

    self.UAVS.mode = VehicleMode("LAND")
    self.UAVS.close()
    self.UAVS.flush()
    
  def run(self):
    ConnectToUAV()
    TakeOff()
    
parser = argparse.ArgumentParser()
parser.add_argument("-input", dest='uInput', type = str, help="whether to run simulated or real uav, 0 or 1", default = 1)
parser.add_argument("-AT", dest='aAltitudeTarget', type = int, help="how high to fly, in meters", default = 10)
parser.add_argument("-FT", dest='aFlyTime', type = int, help="how long to fly, in seconds", default = 10)            
args = parser.parse_args()
main = Main(args.uInput, args.aAltitudeTarget, args.aFlyTime)

try:
  main.run()
except KeyboardInterrupt:
  sys.exit()

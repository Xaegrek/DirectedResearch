inputLaunch = None
altitudeTarget = None
flyTime = None
UAVS = None
GPS = None
kill = False

# Pixhawk ID
PX4n = 2	# number of possible pixhawk id's, for more general control.  May switch it to autodetect in future
PX4ID0 = '/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00'
PX4ID1 = '/dev/serial/by-id/usb-3D_Robotics_PX4_BL_FMU_v2.x_0-if00'

posHistory = []
poshistoryGPS = []
# Attitude, Position, Dynamics
coordinatesGPS = None
infoGPS = None
coordinatesRel = None
uSpeed = 1

# User Input Variables
launchCode = None
N_G = None
skyBox = []

# Relative Coordinate Data Data
a1 = [0,0,10] # north, east, alt
b1 = [5,0,15]
bc1 = [10,0,15]
c1 = [10,5,15]
d1 = [10,15,10]
desiredPath1 = [a1,b1,bc1,c1] #todo: assuming units are metres
tdesiredPath = []
desiredPathDJ = []
smoothPath1 = []

# Trajectory Planning Variables
optimTrajectory = []

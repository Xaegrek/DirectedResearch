from include import globalVariables as gVar

from scipy import interpolate as intp
from scipy import linspace
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time

def simpleArcWaypoint(path):
	# takes:
	# 	current gps position
	# goal:
	# 	path and iterplotae set of GPS cooridanets
	num_true_pts = 50
	pathD = [[],[],[]]
	for i in range(len(path)):
		pathD[0].append(path[i][0])
		pathD[1].append(path[i][1])
		pathD[2].append(path[i][2])
	print(pathD)
	tck, u = intp.splprep(pathD) # todo have this variable number based on desired path
	u_fine = linspace(0, 1, num_true_pts)
	x_fine, y_fine, z_fine = intp.splev(u_fine, tck)
	gVar.smoothPath1 = x_fine, y_fine, z_fine
	print(gVar.smoothPath1)
	# pathD[0],pathD[1],pathD[2]

	fig2 = plt.figure(2)
	ax3d = fig2.add_subplot(111, projection='3d')
	ax3d.plot(pathD[0], pathD[1], pathD[2], 'b')
	ax3d.plot(x_fine, y_fine, z_fine, 'g')
	fig2.show()
	print("tt")
	time.sleep(5)

def run():
	simpleArcWaypoint(gVar.desiredPath1)

run()
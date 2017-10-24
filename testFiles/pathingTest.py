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
	num_true_pts = 4*len(path)
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
	smoothPath = []
	for i in range(len(x_fine)):
		print(i)
		smoothPath.append([x_fine[i], y_fine[i], z_fine[i]])
	print(smoothPath)
	print(gVar.smoothPath1)
	# pathD[0],pathD[1],pathD[2]

	# plots points on figure for viewing
	plt.figure(2)
	plt.subplot(111, projection='3d')
	plt.plot(pathD[0], pathD[1], pathD[2], 'b')
	plt.plot(x_fine, y_fine, z_fine, 'g')

	plt.figure(3)
	plt.subplot(311)
	plt.plot(x_fine)
	plt.ylabel('x position')
	plt.subplot(312)
	plt.plot(y_fine)
	plt.ylabel('y position')
	plt.subplot(313)
	plt.plot(z_fine)
	plt.ylabel('z position')

	plt.show()


def run():
	simpleArcWaypoint(gVar.desiredPath1)

run()
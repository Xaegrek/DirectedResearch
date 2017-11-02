import numpy as sp
import time

############### todo rewrite and learn how this works
from collections import defaultdict


class Digraph(object):
	def __init__(self, nodes=[]):
		self.nodes = set()
		self.neighbours = defaultdict(set)
		self.dist = {}

	def addNode(self, *nodes):
		[self.nodes.add(n) for n in nodes]

	def addEdge(self, frm, to, d=1e309):
		self.addNode(frm, to)
		self.neighbours[frm].add(to)
		self.dist[frm, to] = d

	def dijkstra(self, start, maxD=1e309):
		"""Returns a map of nodes to distance from start and a map of nodes to
		the neighbouring node that is closest to start."""
		# total distance from origin
		tdist = defaultdict(lambda: 1e309)
		tdist[start] = 0
		# neighbour that is nearest to the origin
		preceding_node = {}
		unvisited = self.nodes

		while unvisited:
			current = unvisited.intersection(tdist.keys())
			if not current: break
			min_node = min(current, key=tdist.get)
			unvisited.remove(min_node)

			for neighbour in self.neighbours[min_node]:
				d = tdist[min_node] + self.dist[min_node, neighbour]
				if tdist[neighbour] > d and maxD >= d:
					tdist[neighbour] = d
					preceding_node[neighbour] = min_node

		return tdist, preceding_node

	def min_path(self, start, end, maxD=1e309):
		"""Returns the minimum distance and path from start to end."""
		tdist, preceding_node = self.dijkstra(start, maxD)
		dist = tdist[end]
		backpath = [end]
		try:
			while end != start:
				end = preceding_node[end]
				backpath.append(end)
			path = list(reversed(backpath))
		except KeyError:
			path = None

		return dist, path

	def dist_to(self, *args):
		return self.min_path(*args)[0]

	def path_to(self, *args):
		return self.min_path(*args)[1]


###############

class gridClass:
	n_grid_row = None


class bparam:
	mean = []


class threat_bd:
	basis_parameters = bparam
	n_threat_parameters = None


def calc_basis_value(threat_basis_data, posn):
	H_measurement = sp.zeros((len(posn[0]), threat_basis_data.n_threat_parameters))

	for m1 in range(len(posn[0])):
		posn_vec = posn[0, m1] * sp.ones(threat_basis_data.n_threat_parameters), \
				   posn[1, m1] * sp.ones(threat_basis_data.n_threat_parameters)

		H_measurement[m1, :] = sp.multiply((1 / sp.sqrt(2.0 * sp.pi * (threat_basis_data.basis_parameters.var) ** 2)),
										   sp.exp(
											   sp.multiply((-1 / (2.0 * (threat_basis_data.basis_parameters.var) ** 2)),
														   (sp.square(
															   posn_vec[0] - threat_basis_data.basis_parameters.mean[
																   0]) +
															sp.square(
																posn_vec[1] - threat_basis_data.basis_parameters.mean[
																	1])))))
	return H_measurement


def calc_threat(threat_basis_data, threat_parameters, posn):
	# "posn" is 2x n vector, where each column has 2D position coordinates
	H_measurement = calc_basis_value(threat_basis_data, posn)
	threat_value = threat_basis_data.offset + sp.transpose(sp.matmul(H_measurement, threat_parameters))
	return threat_value


def grid(threat_basis_data, threat_parameters_true, N_G):
	grid_world = gridClass
	# setting up a uniform grid and calculating threat value at any grid point
	grid_world.n_grid_points = N_G ** 2
	grid_world.n_grid_row = N_G
	grid_world.spacing = 2 / (grid_world.n_grid_row - 1)

	grid_world.coordinates = sp.zeros((2, grid_world.n_grid_points))

	for m1 in range(grid_world.n_grid_points):
		grid_world.coordinates[:, m1] = [- 1 + (sp.mod(m1, grid_world.n_grid_row)) * grid_world.spacing,
										 - 1 + sp.floor(m1 / grid_world.n_grid_row) * grid_world.spacing]
	# Calculate threat at each grid point
	threat_value_true = calc_threat(threat_basis_data, threat_parameters_true, grid_world.coordinates)

	return threat_value_true, grid_world


def threatField(N_G):
	# begin defining theat field parameters
	threat_basis_data = threat_bd()
	threat_basis_data.n_threat_parameters = 25

	# Coefficients \theta in the expression for threat field, column vector
	threat_parameters_true = [1.1665, 1.2128, 0.4855, 1.0260, 0.8707, - 0.3818, 0.4289,
							  - 0.2991, - 0.8999, 0.6347, 0.0675, - 0.1871, 0.2917, 0.9877,
							  0.3929, 0.1946, 0.2798, 0.0512, - 0.7745, 0.7868, 1.4089,
							  - 0.5341, 1.9278, - 0.1762, - 0.2438]

	n_center_rows = int(sp.sqrt(threat_basis_data.n_threat_parameters))
	center_spacing = 2.0 / (n_center_rows + 1)

	# Constants \bar{x}_n and \bar{y}_n in the expression for threat field
	threat_basis_data.basis_parameters.mean = sp.zeros((2, threat_basis_data.n_threat_parameters))
	for m1 in range(1, n_center_rows + 1):
		for m2 in range(1, n_center_rows + 1):
			threat_basis_data.basis_parameters.mean[:, (m2 - 1) * n_center_rows + m1 - 1] = \
				[-1 + m1 * center_spacing,
				 -1 + m2 * center_spacing]

	# Constants \nu_n in the expression for threat field
	threat_basis_data.basis_parameters.var = float((1.25 * center_spacing) ** 2)  # This is \sigma^2_\Psi
	print(threat_basis_data.basis_parameters.var)
	# Constant c_offset in the expression for threat field
	threat_basis_data.offset = 3

	# Establish Grid
	[threat_value_true, grid_world] = grid(threat_basis_data, threat_parameters_true, N_G)
	return threat_value_true


def pathingBoundaries(N_G, threat_value_true): #todo create version which connects diagonal vectices
	# setup grid boundaries
	A = sp.zeros((N_G ** 2, N_G ** 2))
	N_Gt = N_G
	for n in range(1, N_G ** 2 + 1):
		nt = n - 1
		if n / N_G <= 1:  # bottom of grid
			A[nt, nt + N_Gt] = 1
			A[nt + N_Gt, nt] = 1
			if n == 1:
				A[nt + 1, nt] = 1
			elif n % N_G == 0:  # right bottom corner of grid
				A[nt - 1, nt] = 1
				A[nt, nt - 1] = 1
			elif n != N_G:
				A[nt - 1, nt] = 1
				A[nt + 1, nt] = 1
				A[nt, nt + 1] = 1
		elif sp.ceil(float(n) / N_G) == N_G:  # top of grid
			A[nt, nt - N_Gt] = 1
			A[nt - N_Gt, nt] = 1
			if n % N_G == 0:  # right top of grid
				A[nt - 1, nt] = 1
			elif n % N_G == 1:  # reft top of grid
				A[nt + 1, nt] = 1
			else:
				A[nt + 1, nt] = 1
				A[nt, nt + 1] = 1
				A[nt - 1, nt] = 1
				A[nt, nt - 1] = 1
		elif n % N_G == 0:  # right of grid
			A[nt - 1, nt] = 1
			A[nt, nt - 1] = 1
			A[nt, nt + N_Gt] = 1
			A[nt, nt - N_Gt] = 1
		elif n % N_G == 1:  # left of grid
			A[nt + 1, nt] = 1
			A[nt, nt + 1] = 1
			A[nt, nt + N_Gt] = 1
			A[nt, nt - N_Gt] = 1
		else:  # inside of grid
			A[nt + 1, nt] = 1
			A[nt - 1, nt] = 1
			A[nt, nt + N_Gt] = 1
			A[nt, nt - N_Gt] = 1

	# define cost limits
	C = sp.zeros((N_G ** 2, N_G ** 2))
	for m1 in range(N_G ** 2):
		for m2 in range(N_G ** 2):
			C[m1, m2] = (threat_value_true[m1] + threat_value_true[m2]) / 2
	graph = sp.multiply(A, C)
	sp.savetxt('guru99.txt', A)
	return graph

def pathToCoordinates(path,gridPoints):
	pathCoordinates = []
	for i in path:	#todo make sure these axises aren't switched
		x = i%gridPoints*-1
		y = int(i/gridPoints)
		coord = [x,y]
		pathCoordinates.append(coord)
	return pathCoordinates

def coorDjik(N_G):
	# N_G corresponds to grid size
	threat_value_true = threatField(N_G)
	graph = pathingBoundaries(N_G, threat_value_true)
	grap = Digraph()
	for i in range(len(graph)):
		grap.addNode(i)
		for j in range(len(graph)):
			# print('ij', i, j, 'dist', graph[i, j])
			if graph[i, j] != 0:
				grap.addEdge(i, j, graph[i, j])

	[v, p] = grap.min_path(0,N_G**2-1) # v is path cost, p is path from a to b
	coor = pathToCoordinates(p,N_G)
	return coor

# c = coorDjik(10)
# print(c)
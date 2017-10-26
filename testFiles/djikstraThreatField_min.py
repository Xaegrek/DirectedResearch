import scipy as sp
import time


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

		H_measurement[m1, :] = sp.multiply((1 / sp.sqrt(2 * sp.pi * (threat_basis_data.basis_parameters.var) ** 2)),
											sp.exp(
												sp.multiply((-1 / (2 * (threat_basis_data.basis_parameters.var) ** 2)),
															(sp.square(
																posn_vec[0] - threat_basis_data.basis_parameters.mean[0]) +
															sp.square(
																posn_vec[1] - threat_basis_data.basis_parameters.mean[1])))))
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
	center_spacing = 2 / (n_center_rows + 1)

	# Constants \bar{x}_n and \bar{y}_n in the expression for threat field
	threat_basis_data.basis_parameters.mean = sp.zeros((2, threat_basis_data.n_threat_parameters))
	for m1 in range(1,n_center_rows+1):
		for m2 in range(1,n_center_rows+1):
			threat_basis_data.basis_parameters.mean[:, (m2-1) * n_center_rows + m1-1] = \
				[-1+m1 * center_spacing,
				 -1+m2 * center_spacing]

	# Constants \nu_n in the expression for threat field
	threat_basis_data.basis_parameters.var = (1.25 * center_spacing) ** 2  # This is \sigma^2_\Psi

	# Constant c_offset in the expression for threat field
	threat_basis_data.offset = 3

	# Establish Grid
	[threat_value_true, grid_world] = grid(threat_basis_data, threat_parameters_true, N_G)
	return threat_value_true

def pathingBoundaries(N_G, threat_value_true):
	# setup grid boundaries
	A = sp.zeros((N_G ** 2, N_G ** 2))
	N_Gt = N_G
	for n in range(1, N_G ** 2):
		nt = n - 1
		if n / N_G <= 1:
			A[nt, nt + N_Gt] = 1
			A[nt + N_Gt, nt] = 1
			if n == 1:
				A[nt + 1, nt] = 1
			elif n % N_G == 0:
				A[nt - 1, nt] = 1
				A[nt, nt - 1] = 1
			elif n != N_G:
				A[nt - 1, nt] = 1
				A[nt + 1, nt] = 1
				A[nt, nt + 1] = 1
		elif sp.ceil(n / N_G) == N_G:
			A[nt, nt - N_Gt] = 1
			A[nt - N_Gt, nt] = 1
			if n % N_G == 0:
				A[nt - 1, nt] = 1
			elif n % N_G == 1:
				A[nt + 1, nt] = 1
			else:
				A[nt + 1, nt] = 1
				A[nt, nt + 1] = 1
				A[nt - 1, nt] = 1
				A[nt, nt - 1] = 1
		elif n % N_G == 0:
			A[nt - 1, nt] = 1
			A[nt, nt - 1] = 1
			A[nt, nt + N_Gt] = 1
			A[nt, nt - N_Gt] = 1
		elif n % N_G == 1:
			A[nt + 1, nt] = 1
			A[nt, nt + 1] = 1
			A[nt, nt + N_Gt] = 1
			A[nt, nt - N_Gt] = 1
		else:
			A[nt + 1, nt] = 1
			A[nt - 1, nt] = 1
			A[nt, nt + N_Gt] = 1
			A[nt, nt - N_Gt] = 1

	# define cost limits
	C = sp.zeros((N_G ** 2, N_G ** 2))
	for m1 in range(N_G ** 2):
		for m2 in range(N_G ** 2):
			C[m1, m2] = (threat_value_true[m1] + threat_value_true[m2]) / 2
	return A, C

def djikstra(A,C):
	costs=[]
	path = []
	

	return costs,paths

def run():
	N_G = 5  # corresponds to grid size
	threat_value_true = threatField(N_G)
	[A, C] = pathingBoundaries(N_G, threat_value_true)
	djikstra(A,C)


run()
# todo check all multiplication, as matrices require a special function
# todo cost values are incorrect when compared to matlab script

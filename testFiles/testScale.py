from include import globalVariables as gVar

def scalePath(path):	#todo this, right now i'll just have it fail on a bad shape

	c = None
	nb = 0
	nt = 0
	eb = 0
	et = 0
	zb = 0
	zt = 0

	for i in range(len(path)):
		if path[i,0] < gVar.skyBox[2] and path[i,0] != abs(path[i,0]):
			gVar.kill = True
		elif path[i,0] > gVar.skyBox[3] and nt < abs(float(gVar.skyBox[3])/float(path[i,0])) :
			nt = abs(float(gVar.skyBox[3])/float(path[i,0]))
		elif path[i,1] < gVar.skyBox[4] and eb < abs(float(gVar.skyBox[4])/float(path[i,0])):
			eb = abs(float(gVar.skyBox[4])/float(path[i,0]))
		elif path[i,1] > gVar.skyBox[5] and et < abs(float(gVar.skyBox[5])/float(path[i,0])):
			et = abs(float(gVar.skyBox[5])/float(path[i,0]))
		try:
			if path[i, 3] < gVar.skyBox[0] and zb < abs(float(gVar.skyBox[0]) / float(path[i, 0])):
				zb = abs(float(gVar.skyBox[0]) / float(path[i, 0]))
		except:
			pass
		try:
			if path[i, 3] > gVar.skyBox[1] and zt < abs(float(gVar.skyBox[1]) / float(path[i, 0])):
				zt = abs(float(gVar.skyBox[1]) / float(path[i, 0]))
		except:
			pass

	for i in range(len(path)):
		path[i,0] = path[i,0] * c

	return

print
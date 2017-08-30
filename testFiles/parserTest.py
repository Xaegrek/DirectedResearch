from include import globalVariables as gVar
import argparse
import sys
class Main:
	def __init__(self, uInput):
		gVar.inputLaunch = uInput

	def run(self):
		print(gVar.inputLaunch)
		return


parser = argparse.ArgumentParser()
parser.add_argument("-input", dest='uInput', type=str, help="whether to run simulated or real uav, 0 or 1", default="1")
args = parser.parse_args()
main = Main(args.uInput)

try:
	main.run()
except KeyboardInterrupt:
	sys.exit()
import sys
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

def isValidArguments(arguments):
	options = ["evaluate", "globalrate", "globalmean", "average"]
	for argument in arguments:
		if argument not in options:
			return False
	return True

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [<evaluate>] [<globalrate>] [<globalmean>] [<average>]")
		sys.exit(1)
	if not isValidArguments(argv[2:]):
		print("Usage:", sys.argv[0], "<ecosystem> [<evaluate>] [<globalrate>] [<globalmean>] [<average>]")
		sys.exit(1)
	if len(sys.argv) == 2:
		print("no options provided. calculating all metrics")
		options = [argument for argument in argv[2:]]
	else:
		options = ["evaluate", "globalrate", "globalmean", "average"]
	ecosystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	if "evaluate" in options:
		print("evaluating edges")
		ecosystemDataManager.evaluateEdges()
		print("saving")
		ecosystemDataManager.save()
		print("done")
	else:
		print("assuming that edges are already evaluated")
	if "globalrate" in options and "globalmean" in options:
		print("calculating both globalrate and globalmean metrics")
		ecosystemDataManager.calculateGlobalRegularityMetrics()
	elif "globalrate" in options or "globalmean" in options:
		print("calculate globalrate and globalmean together is faster")
		if "globalrate" in options:
			print("calculating globalrate")
			ecosystemDataManager.calculateGlobalRegularityRate()
		elif "globalmean" in options:
			print("calculating globalmean")
			ecosystemDataManager.calculateGlobalRegularityMean()
		print("saving")
		ecosystemDataManager.save()
		print("done")
	if "average" in options:
		print("calculating average")
		ecosystemDataManager.average()
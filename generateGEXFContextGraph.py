import sys
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager
from ecosystemDataManager.package import Package
from ecosystemDataManager.version import Version
from ecosystemDataManager.dependency import Dependency
from ecosystemDataManager.occurrence import Occurrence

PARENT_VERTICES = []
OCCURRENCE_EDGES = []
DESCENDENT_VERTICES = []
DEPENDENCY_EDGES = []
FILE = None

def getOccurrences(entity):
	if type(entity) == Version:
		return entity.getOccurrences()
	elif type(entity) == Package:
		return entity.getPackagesOccurrences()
	else:
		raise Exception

def getDependencies(entity):
	if type(entity) == Version:
		return entity.getDependencies()
	elif type(entity) == Package:
		return entity.getPackagesDependencies()
	else:
		raise Exception

def getInVersion(entity):
	if type(entity) == Dependency or type(entity) == Occurrence:
		return entity.getInVersion()
	elif type(entity) == Package:
		return entity
	else:
		raise Exception

def generateOccurrences(entity):
	if entity in PARENT_VERTICES:
		return
	PARENT_VERTICES.append(entity)
	for occurrence in getOccurrences(entity):
		OCCURRENCE_EDGES.append((getInVersion(occurrence), entity))
		generateOccurrences(getInVersion(occurrence))

def generateDependencies(entity):
	if entity in DESCENDENT_VERTICES:
		return
	DESCENDENT_VERTICES.append(entity)
	for dependency in getDependencies(entity):
		DEPENDENCY_EDGES.append((entity, getInVersion(dependency)))
		generateDependencies(getInVersion(dependency))

def getAttributes(entity):
	attributes = {}
	size = 3
	if type(entity) == Version:
		globalRegularityRate = entity.getGlobalRegularityRate()
	else:
		globalRegularityRate = 0 if entity.isIrregular() else 1
	if (globalRegularityRate == 0):
		r = 249
		g = 22
		b = 22
		size = 3.5
	elif (globalRegularityRate == 1):
		r = 49
		g = 249
		b = 22
	elif (globalRegularityRate <= 0.25):
		r = 255
		g = 133
		b = 20
	elif (globalRegularityRate > 0.25 and globalRegularityRate <= 0.75):
		r = 255
		g = 235
		b = 20
	elif (globalRegularityRate > 0.75):
		r = 20
		g = 129
		b = 255
	attributes["red"] = r
	attributes["green"] = g
	attributes["blue"] = b
	attributes["alpha"] = 0.5
	attributes["size"] = size
	attributes["shape"] = "disc"
	return attributes

"""
Generate a directed graph by package in ecosystem, this graph most be read by Gephi
"""
def generateGraph(entity):
	generateDependencies(entity)
	generateOccurrences(entity)
	FILE.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
	FILE.write("<gexf xmlns=\"http://www.gexf.net/1.2draft\" xmlns:viz=\"http://www.gexf.net/1.1draft/viz\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd\" version=\"1.2\">")
	FILE.write("<graph>")
	FILE.write("<nodes>")
	FILE.write("<node id=\"" + str(entity) + "\" label=\"" + str(entity) + "\"> <viz:color r=\"22\" g=\"66\" b=\"186\" a=\"1\"/> <viz:size value=\"3\"/> <viz:shape value=\"disc\"/></node>")
	for vertex in PARENT_VERTICES:
		attributes = getAttributes(vertex)
		r = attributes["red"]
		g = attributes["green"]
		b = attributes["blue"]
		size = attributes["size"]
		FILE.write("<node id=\"" + str(vertex) + "\" label=\"" + str(vertex) + "\"> <viz:color r=\""+str(r)+"\" g=\""+str(g)+"\" b=\""+str(b)+"\" a=\"0.5\"/> <viz:size value=\""+str(size)+"\"/> <viz:shape value=\"disc\"/></node>")
	for vertex in DESCENDENT_VERTICES:
		attributes = getAttributes(vertex)
		r = attributes["red"]
		g = attributes["green"]
		b = attributes["blue"]
		size = attributes["size"]
		FILE.write("<node id=\"" + str(vertex) + "\" label=\"" + str(vertex) + "\"> <viz:color r=\""+str(r)+"\" g=\""+str(g)+"\" b=\""+str(b)+"\" a=\"1\"/> <viz:size value=\""+str(size)+"\"/> <viz:shape value=\"disc\"/></node>")
	FILE.write("</nodes>")
	FILE.write("<edges>")
	i = 0
	for edge in OCCURRENCE_EDGES:
		r = 249
		g = 22
		b = 22
		if (edge[1].isIrregular()):
			r = 49
			g = 249
			b = 22
		FILE.write("<edge id=\"" + str(i) + "\" source=\"" + str(edge[0]) + "\" target=\"" + str(edge[1]) + "\"><viz:color r=\""+str(r)+"\" g=\""+str(g)+"\" b=\""+str(b)+"\" a=\"0.2\"/></edge>")
		i += 1
	for edge in DEPENDENCY_EDGES:
		r = 249
		g = 22
		b = 22
		if (edge[0].isIrregular()):
			r = 49
			g = 249
			b = 22
		FILE.write("<edge id=\"" + str(i) + "\" source=\"" + str(edge[0]) + "\" target=\"" + str(edge[1]) + "\"><viz:color r=\""+str(r)+"\" g=\""+str(g)+"\" b=\""+str(b)+"\" a=\"0.6\"/></edge>")
		i += 1
	FILE.write("</edges>")
	FILE.write("</graph>")
	FILE.write("</gexf>")

if __name__ == '__main__':
	package = None
	version = None
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [[package|version] [<package> [<version>]]]")
		sys.exit(1)
	elif len(sys.argv) > 2:
		if sys.argv[2] != "package" and sys.argv[2] != "version":
			print("Usage:", sys.argv[0], "<ecosystem> [[package|version] [<package> [<version>]]]")
			sys.exit(1)
		graphType = sys.argv[2]
		if len(sys.argv) > 3:
			package = sys.argv[3]
		if len(sys.argv) > 4:
			version = sys.argv[4]
	else:
		graphType = "version"
	ecosystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	if package:
		package = ecosystemDataManager.getPackage(package)
	else:
		print("no package provided. Retrieving Most Popular")
		package = ecosystemDataManager.getMostPopularPackages(1)[0]
	if graphType == "version":
		if version:
			version = package.getVersion(version)
		else:
			print("no version provided. Retrieving Most Popular")
			version = package.getMostPopularVersions(1)[0]
		print("generating GEXF to", version)
		with open(ecosystem + "_" + package.getName() + "_" + version.getName() + ".gexf", "w") as FILE:
			generateGraph(version)
		print("done")
	else:
		with open(ecosystem + "_" + package.getName() + ".gexf", "w") as FILE:
			generateGraph(package)
		print("done")
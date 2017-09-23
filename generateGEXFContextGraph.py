import sys
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

EDGES_OCURRENCES = []
VERTICES_OCURRENCES = []
EDGES_DEPENDENCIES = []
VERTICES_DEPENDENCIES = []

def buildTreePackageDependencies(version):
	if version in VERTICES_DEPENDENCIES:
		return
	VERTICES_DEPENDENCIES.append(version)
	for dependency in version.getDependencies():
		EDGES_DEPENDENCIES.append((version, dependency.getInVersion()))
		buildTreePackageDependencies(dependency.getInVersion())

def buildTreePackageOcurrences(version):
	if version in VERTICES_OCURRENCES:
		return
	VERTICES_OCURRENCES.append(version)
	for ocurrence in version.getOcurrences():
		EDGES_OCURRENCES.append((ocurrence.getInVersion(), version))
		buildTreePackageOcurrences(ocurrence.getInVersion())

def generateXmlGraph(version):
	treePackage = []
	treePackage.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
	treePackage.append("<gexf xmlns=\"http://www.gexf.net/1.2draft\" xmlns:viz=\"http://www.gexf.net/1.1draft/viz\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd\" version=\"1.2\"> \n")
	treePackage.append("<graph> \n <nodes>")
	treePackage.append("<node id=\"" + str(version) + "\" label=\"" + str(version) + "\"> <viz:color r=\"22\" g=\"66\" b=\"186\" a=\"0.5\"/> <viz:size value=\"3\"/> <viz:shape value=\"disc\"/></node>")
	for vertex in VERTICES_OCURRENCES:
		treePackage.append("<node id=\"" + str(vertex) + "\" label=\"" + str(vertex) + "\"> <viz:color r=\"113\" g=\"203\" b=\"157\" a=\"0.5\"/> <viz:size value=\"3\"/> <viz:shape value=\"disc\"/></node>")

	for vertex in VERTICES_DEPENDENCIES:
		treePackage.append("<node id=\"" + str(vertex) + "\" label=\"" + str(vertex) + "\"> <viz:color r=\"113\" g=\"203\" b=\"157\" a=\"1\"/> <viz:size value=\"3\"/> <viz:shape value=\"disc\"/></node>")

	treePackage.append("</nodes> \n <edges>")
	
	i = 0
	for edge in EDGES_OCURRENCES:
		treePackage.append("<edge id=\"" + str(i) + "\" source=\"" + str(edge[0]) + "\" target=\"" + str(edge[1]) + "\"><viz:color r=\"0\" g=\"0\" b=\"0\" a=\"0.5\"/></edge>")
		i += 1

	for edge in EDGES_DEPENDENCIES:
		treePackage.append("<edge id=\"" + str(i) + "\" source=\"" + str(edge[0]) + "\" target=\"" + str(edge[1]) + "\"><viz:color r=\"100\" g=\"100\" b=\"100\" a=\"1\"/></edge>")
		i += 1

	treePackage.append("</edges> \n </graph> \n </gexf>")

	with open('ecosystem_package_version.gexf', 'w') as file:
		for line in treePackage:
			file.write(str(line + "\n"))

if __name__ == '__main__':
	package = None
	version = None
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecossystem> [[package|version] [<package> [<version>]]]")
		sys.exit(1)
	elif len(sys.argv) > 2:
		if sys.argv[2] != "package" and sys.argv[2] != "version":
			print("Usage:", sys.argv[0], "<ecossystem> [[package|version] [<package> [<version>]]]")
			sys.exit(1)
		graphType = sys.argv[2]
		if len(sys.argv) > 3:
			package = sys.argv[3]
		if len(sys.argv) > 4:
			version = sys.argv[4]
	else:
		graphType = "version"
	ecossystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecossystem)
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
		buildTreePackageOcurrences(version)
		buildTreePackageDependencies(version)
		generateXmlGraph(version)
		print("done")
	else:
		print("notImplementedYet")
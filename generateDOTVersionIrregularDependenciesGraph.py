import sys
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

VISITED = []
FILE = None

"""
Write in file the struct to by read in DOT generator
To generate DOT in PDF use the comand: dot -Tpdf > file.pdf
"""
def generate(version):
	if version in VISITED:
		return
	VISITED.append(version)
	if not version.getDatetime():
		return
	color = "red" if version.isIrregular() == True else "orange" if version.isAffected() == True else "blue"
	licenses = ", ".join([str(l) for l in version.getLicenses()])
	if not licenses:
		licenses = "none"
	FILE.write("\"" + str(version) + "\\n" + licenses + "\"" + "[color="+color+"]" + ";")
	for d in version.getDependencies():
		inV = d.getInVersion()
		if inV.isAffected() == False and inV.isIrregular() == False and d.isIrregular() == False:
			continue
		outV = d.getOutVersion()
		outL = ", ".join([str(l) for l in outV.getLicenses()])
		if not outL:
			outL = "none"
		inL = ", ".join([str(l) for l in inV.getLicenses()])
		if not inL:
			inL = "none"
		color = "red" if d.isIrregular() == True else "green" if d.isIrregular() == False else "gray"
		FILE.write("\"" + str(outV) + "\\n" + outL + "\"" + "->" + "\"" + str(inV) + "\\n" + inL + "\"" + "[color=" + color + "]" + ";")
		generate(inV)

"""
Generate a directed graphs from package of ecosystem
"""
def generateDot(version):
	FILE.write("digraph graphname {")
	generate(version)
	FILE.write("}")

if __name__ == '__main__':
	package = None
	version = None
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [<package> [<version>]]")
		sys.exit(1)
	if len(sys.argv) > 2:
		package = sys.argv[2]
	if len(sys.argv) > 3:
		version = sys.argv[3]
	ecosystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	if package:
		package = ecosystemDataManager.getPackage(package)
	else:
		print("no package provided. Retrieving Most Popular")
		package = ecosystemDataManager.getMostPopularPackages(1)[0]
	if version:
		version = package.getVersion(version)
	else:
		print("no version provided. Retrieving Most Popular")
		version = package.getMostPopularVersions(1)[0]
	print("generating DOT to", version)
	with open(ecosystem + "_" + package.getName() + "_" + version.getName() + ".dot", "w") as FILE:
		generateDot(version)
	print("done")
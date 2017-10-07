from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager
import csv
import sys

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [<file>]")
		sys.exit(1)
	if len(sys.argv) > 2:
		file = sys.argv[2]
	else:
		print("file not provided. using default.")
		file = "export.csv"
	try:
		open(file)
		print("file loaded")
		file = open(file, "a")
		file = csv.writer(file, delimiter = ';')
	except Exception as e:
		file = open(file, "w")
		file = csv.writer(file, delimiter = ';')
		file.writerow(["ecosystem","package","version","licenses","dependencies","ocurrences","parents","downloads","localrate","globalrate","globalmean"])
		print("file not loaded. initialized.")
	ecosystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	for package in ecosystemDataManager.getPackages():
		for version in package.getVersions():
			if not version.getDatetime():
				continue
			file.writerow([ecosystem,package,version,len(version.getLicenses()),len(version.getDependencies()),len(version.getOcurrences()),version.getContextSize(),version.getDownloads(),version.getLocalRegularityRate(),version.getGlobalRegularityRate(),version.getGlobalRegularityMean()])
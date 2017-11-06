from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager
from ecosystemDataManager.group import Group
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
		file = "licensesChanges.csv"
	try:
		open(file)
		print("file loaded")
		file = open(file, "a")
		file = csv.writer(file, delimiter = ';')
	except Exception as e:
		file = open(file, "w")
		file = csv.writer(file, delimiter = ';')
		file.writerow(["ecosystem","package","versions","unknownTOknown", "knownTOunknown", "latestGroup"])
		print("file not loaded. initialized.")
	ecosystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	for package in ecosystemDataManager.getPackages():
		unknownTOknown = 0
		knownTOunknown = 0
		history = package.getHistory()
		for i in range(len(history) - 1):
			versionFrom = history[i]
			versionTo = history[i + 1]
			if not versionFrom.getDatetime():
				continue
			if not versionTo.getDatetime():
				continue
			licensesFrom = versionFrom.getLicenses()
			licensesTo = versionTo.getLicenses()
			if not licensesFrom:
				if licensesTo:
					for licenseTo in licensesTo:
						groupTo = licenseTo.getGroup()
						if groupTo == Group.KNOWN:
							unknownTOknown += 1
			elif not licensesTo:
				for licenseFrom in licensesFrom:
					groupFrom = licenseFrom.getGroup()
					if groupFrom == Group.KNOWN:
						knownTOunknown += 1
			else:
				groupsFrom = [license.getGroup().value for license in licensesFrom]
				groupsTo = [license.getGroup().value for license in licensesFrom]
				if groupsFrom == groupsTo:
					continue
				for licenseFrom in licensesFrom:
					for licenseTo in licensesTo:
						groupFrom = licenseFrom.getGroup()
						groupTo = licenseTo.getGroup()
						if groupFrom == Group.KNOWN:
							if groupTo == Group.NONE or groupTo == Group.UNDEFINED:
								knownTOunknown += 1
						if groupFrom == Group.NONE or groupFrom == Group.UNDEFINED:
							if groupTo == Group.KNOWN:
								unknownTOknown += 1
		try:
			if unknownTOknown > 0 or knownTOunknown > 0:
				versions = len(package)
				if package.getLatestVersion().getLicenses():
					latestGroup = ",".join([license.getGroup().name for license in package.getLatestVersion().getLicenses()])
				else:
					latestGroup = Group.NONE.name
				file.writerow([ecosystem, package, versions, unknownTOknown, knownTOunknown, latestGroup])
		except Exception as e:
			print(package, len(package), "discarted")
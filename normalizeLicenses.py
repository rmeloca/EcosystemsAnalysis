import sys
import json
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

"""

"""
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [<licenses> <normalized>]")
		sys.exit(1)
	ecosystem = sys.argv[1]
	if len(sys.argv) > 3:
		normalized = sys.argv[3]
		licenses = sys.argv[2]
	else:
		print("normalized not provided. using default.")
		normalized = "normalized.json"
		if len(sys.argv) > 2:
			licenses = sys.argv[2]
		else:
			print("licenses not provided. using default.")
			licenses = "licenses.json"
	licenses = json.load(open(licenses))
	normalized = json.load(open(normalized))
	if len(licenses) != len(normalized):
		print("licenses and normalized length are not equal. aborting.")
		sys.exit(1)
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	backup = input("this is a destructive operation! Do you want to backup licenses? Backup if any will be replaced. [y/n]: ")
	if backup == "y":
		ecosystemDataManager.backupLicenses()
	packages = ecosystemDataManager.getPackages()
	for package in packages:
		for version in package.getVersions():
			originalLicenses = version.get("VersionsHasLicenses")
			normalizedLicenses = []
			for license in originalLicenses:
				try:
					replaceTo = normalized[licenses.index(license)]
				except Exception as e:
					replaceTo = license
				if type(replaceTo) == str:
					normalizedLicenses.append(replaceTo)
				elif type(replaceTo) == list:
					normalizedLicenses += replaceTo
			version.setLicenses(normalizedLicenses)
	ecosystemDataManager.save()
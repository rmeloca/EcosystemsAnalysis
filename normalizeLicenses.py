import sys
import json
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecossystem> [<licenses> <normalized>]")
		sys.exit(1)
	if len(sys.argv) == 3:
		print("Usage:", sys.argv[0], "<ecossystem> [<licenses> <normalized>]")
		sys.exit(1)
	ecossystem = sys.argv[1]
	if len(sys.argv) > 3:
		licenses = sys.argv[2]
		normalized = sys.argv[3]
	else:
		licenses = "licenses.json"
		normalized = "normalized.json"
	licenses = json.load(open(licenses))
	normalized = json.load(open(normalized))
	ecosystemDataManager = EcosystemDataManager(ecossystem)
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
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
		file = "versionsWithUnknownLicenses.csv"
	try:
		open(file)
		print("file loaded")
		file = open(file, "a")
		file = csv.writer(file, delimiter = ';')
	except Exception as e:
		file = open(file, "w")
		file = csv.writer(file, delimiter = ';')
		file.writerow(["ecosystem","package","version","group","author","email","repository","licenses","normalized","parents"])
		print("file not loaded. initialized.")
	ecosystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	for package in ecosystemDataManager.getPackages():
		for version in package.getVersions():
			if not version.getDatetime():
				continue
			for license in version.getLicenses():
				if license.getGroup() == Group.NONE or license.getGroup() == Group.UNKNOWN or license.getGroup() == Group.UNDEFINED:
					group = license.getGroup().name
					author = version.getAuthor()
					email = version.getEmail()
					repository = package.getRepository()
					licenses = ", ".join(version.getOriginalLicenses())
					normalized = ", ".join([str(license) for license in version.getLicenses()])
					parents = version.getContextSize()
					file.writerow([ecosystem, package, version, group, author, email, repository, licenses, normalized, parents])
					break
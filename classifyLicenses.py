import sys
import json
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager
from ecosystemDataManager.group import Group

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [<osi> [<unlisted>]]")
		sys.exit(1)
	if len(sys.argv) > 4:
		unlisted = sys.argv[3]
	else:
		unlisted = "unlisted.json"
		print("Unlisted not provided, using default")
		if len(sys.argv) > 3:
			osi = sys.argv[2]
		else:
			print("OSI not provided, using default")
			osi = "osi.json"
	ecosystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	packages = ecosystemDataManager.getPackages()
	try:
		with open(osi) as file:
			osi = json.load(file)
			print("OSI loaded")
	except Exception as e:
		osi = []
		print("OSI not loaded")
	try:
		with open(unlisted) as file:
			unlisted = json.load(file)
			print("Unlisted loaded")
	except Exception as e:
		print("Unlisted not loaded")
		unlisted = []
	for package in packages:
		for version in package.getVersions():
			for license in version.getLicenses():
				if license == "none":
					license.setGroup(Group.UNDEFINED)
				elif license == "file":
					license.setGroup(Group.FILE)
				elif license == "copyright":
					license.setGroup(Group.COPYRIGHT)
				elif license in unlisted:
					license.setGroup(Group.UNAPPROVED)
				elif license in osi:
					license.setGroup(Group.KNOWN)
				else:
					license.setGroup(Group.MISUSED)
	ecosystemDataManager.save()
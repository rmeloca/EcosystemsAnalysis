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
	incomplete = "incomplete.json"
	try:
		with open(incomplete) as file:
			incomplete = json.load(file)
			print("incomplete loaded")
	except Exception as e:
		print("incomplete not loaded")
		incomplete = []

	versionsHasLicenses = ecosystemDataManager.get("VersionsHasLicenses")
	licensesHasGroup = ecosystemDataManager.get("LicensesHasGroup")
	for i in range(len(versionsHasLicenses)):
		version = versionsHasLicenses[i]
		for j in range(len(version)):
			license = version[j]
			if license == "none":
				licensesHasGroup[i][j] = Group.NONE.value
			elif license == "file":
				licensesHasGroup[i][j] = Group.FILE.value
			elif license == "copyright":
				licensesHasGroup[i][j] = Group.COPYRIGHT.value
			elif license in unlisted:
				licensesHasGroup[i][j] = Group.UNAPPROVED.value
			elif license in osi:
				licensesHasGroup[i][j] = Group.KNOWN.value
			elif license in incomplete:
				licensesHasGroup[i][j] = Group.UNDEFINED.value
			else:
				licensesHasGroup[i][j] = Group.MISUSED.value
	ecosystemDataManager.save("LicensesHasGroup")

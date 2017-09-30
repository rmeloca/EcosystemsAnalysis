from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager
import csv
import sys

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [<home>]")
		sys.exit(1)
	if len(sys.argv) > 2:
		home = sys.argv[2]
	else:
		home = ""

	ecosystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecosystem, home)
	iregularPackages = ecosystemDataManager.getIregularPackages()

	with open(ecosystem + "Emails.csv", 'w', newline = '') as csvfile:
		file = csv.writer(csvfile, delimiter = ';')

		email = "E-mail"
		packageName = "Package Name"
		tags = "Tags"
		firstInsertion = "First Insertion"
		repository = "Repository"
		iregularVersions = "Versions"
		dependenciesSize = "Dependency Number"
		author = "Author"
		downloads = "Downloads Number"
		licenses = "Licenses"

		file.writerow([email, packageName, tags, firstInsertion, repository, iregularVersions, dependenciesSize, author, downloads, licenses])

		for package in iregularPackages:
			iregularVersions = package.getIregularVersions()
			iregularVersion = iregularVersions[0]
			iregularVersions = ",".join([version.getName() for version in iregularVersions])
			iregularityType = None
			email = iregularVersion.getEmail()
			packageName = package.getName()
			tags = ", ".join([str(tag) for tag in package.getTags()])
			try:
				firstInsertion = package.getFirstInsertion()
			except Exception as e:
				firstInsertion = None
			repository = package.getRepository()
			dependenciesSize = len(package.getDependencies())
			author = iregularVersion.getAuthor()
			downloads = iregularVersion.getDownloads()
			licenses = ", ".join(iregularVersion.getOriginalLicenses())

			file.writerow([email, packageName, tags, firstInsertion, repository, iregularVersions, dependenciesSize, author, downloads, licenses])
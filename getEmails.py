from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager
import csv
import sys

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecossystem> [<home>]")
		sys.exit(1)
	if len(sys.argv) > 2:
		home = sys.argv[2]
	else:
		home = ""

	ecossystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecossystem, home)
	irregularPackages = ecosystemDataManager.getIrregularPackages()

	with open(ecossystem + "Emails.csv", 'w', newline = '') as csvfile:
		file = csv.writer(csvfile, delimiter = ';')

		email = "E-mail"
		package_name = "Package Name"
		tags = "Tags"
		first_insertion = "Fisrt Insertion"
		repository = "Repository"
		problem_version = "Version"
		dependency_number = "Dependency Number"
		author = "Author"
		downloads_number = "Downloads Number"
		license = "License"

		file.writerow([email, package_name, tags, first_insertion, repository, problem_version, dependency_number, author, downloads_number, license])

		for package in irregularPackages:
			irregularVersions = package.getIrregularVersions()
			problem_version = irregularVersions[0]

			email = problem_version.getEmail()
			package_name = package.getName()
			tags = ", ".join([str(tag) for tag in package.getTags()])
			try:
				first_insertion = package.getFirstInsertion()
			except Exception as e:
				first_insertion = "n/a"
			repository = package.getRepository()
			dependency_number = len(package.getDependencies())
			author = problem_version.getAuthor()
			downloads_number = problem_version.getDownloads()
			license = ", ".join([str(license) for license in problem_version.getLicenses()])

			file.writerow([email, package_name, tags, first_insertion, repository, problem_version, dependency_number, author, downloads_number, license])
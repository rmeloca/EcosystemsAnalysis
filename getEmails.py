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
	packages = ecosystemDataManager.getPackages()

	with open(ecossystem+"Email.csv", 'w', newline='') as csvfile:
		file = csv.writer(csvfile, delimiter=',', quotechar=';', quoting=csv.QUOTE_MINIMAL)

		email = "E-mail"
		package_name = "Package Name"
		tags = "Tags"
		first_insertion = "Fisrt Insertion"
		repository = "Repository"
		problem_version = "Version"
		dependency_number = "Dependency Number"
		author = "Author"
		downloads_number = "Downloads Number"
		line_code_number = "Line Code Number"
		license = "License"
		normalized_license = "Normalized License"

		file.writerow([email,package_name,tags,first_insertion,repository,problem_version,dependency_number,author,downloads_number,line_code_number, license])

		for package in packages:

			problem_version = package.getIrregularVesions()[0]
			
			email = problem_version.getEmail()
			package_name = package.getName()
			tags = package.getTags()
			first_insertion = package.getFirstInsertion()
			repository = package.getRepository()
			dependency_number = len(package.getDependencies()) 
			author = problem_version.getAuthor()
			downloads_number = problem_version.getAuthor()
			line_code_number = problem_version.getLinesOfCode()
			license = problem_version.getLicenses()
			

			file.writerow([email,package_name,tags,first_insertion,repository,problem_version,dependency_number,author,downloads_number,line_code_number, license])
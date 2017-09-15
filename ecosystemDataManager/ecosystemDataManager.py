import json
import sys
import os
from .package import Package

class EcosystemDataManager(object):
	"""docstring for EcosystemDataManager"""
	def __init__(self, ecosystem, home = ""):
		super(EcosystemDataManager, self).__init__()
		self.home = home
		self.ecosystem = ecosystem
		self.initialize()
		self.reset()
		self.load("PackagesHasIndex")

	def initialize(self):
		try:
			os.makedirs(self.getPath())
		except Exception as e:
			pass

	def reset(self):
		self.attributes = {}
		self.attributes["PackagesHasIndex"] = []
		self.attributes["PackagesHasMap"] = {}
		self.attributes["PackagesHasVersions"] = []
		self.attributes["PackagesHasOcurrences"] = []
		self.attributes["PackagesHasTags"] = []
		self.attributes["PackagesHasRepository"] = []

		self.attributes["VersionsHasIndex"] = []
		self.attributes["VersionsHasPackage"] = []
		self.attributes["VersionsHasOcurrences"] = []
		self.attributes["VersionsHasGlobalRegularityRate"] = []
		self.attributes["VersionsHasLocalRegularityRate"] = []
		self.attributes["VersionsHasAuthor"] = []
		self.attributes["VersionsHasEmail"] = []
		self.attributes["VersionsHasContextSize"] = []
		self.attributes["VersionsHasDatetime"] = []
		self.attributes["VersionsHasDownloads"] = []
		self.attributes["VersionsHasLinesOfCode"] = []

		self.attributes["VersionsHasLicenses"] = []
		self.attributes["LicensesHasGroup"] = []

		self.attributes["VersionsHasDependencies"] = []
		self.attributes["DependenciesAreIrregular"] = []
		self.attributes["DependenciesHasDelimiter"] = []
		self.attributes["DependenciesHasRequirements"] = []

	def getPath(self, filename = "", extension = ""):
		if extension:
			extension = "." + extension
		return os.path.join(self.home, self.ecosystem, filename + extension)

	def save(self, attribute = None):
		if attribute:
			with open(self.getPath(attribute, "json"), "w") as file:
				file.write(json.dumps(self.attributes[attribute], separators=(',', ':')))
		else:
			for attribute in self.attributes:
				if self.attributes[attribute]:
					self.save(attribute)

	def load(self, attribute = None):
		if attribute:
			try:
				with open(self.getPath(attribute, "json")) as file:
					self.attributes[attribute] = json.load(file)
			except Exception as e:
				self.save(attribute)
		else:
			for attribute in self.attributes:
				self.load(attribute)

	def get(self, attribute):
		if not self.attributes[attribute]:
			self.load(attribute)
		return self.attributes[attribute]

	def getPackageByIndex(self, index):
		if index < 0:
			raise Exception
		try:
			return Package(self, index)
		except Exception as e:
			raise e

	def addPackage(self, name):
		packagesHasMap = self.get("PackagesHasMap")
		try:
			packagesHasMap[name]
		except Exception as e:
			packagesHasIndex = self.get("PackagesHasIndex")
			packagesHasVersions = self.get("PackagesHasVersions")
			packagesHasOcurrences = self.get("PackagesHasOcurrences")
			packagesHasRepository = self.get("PackagesHasRepository")
			packagesHasTags = self.get("PackagesHasTags")

			packagesHasMap[name] = len(packagesHasIndex)
			packagesHasIndex.append(name)
			packagesHasVersions.append({})
			packagesHasOcurrences.append([])
			packagesHasRepository.append(None)
			packagesHasTags.append([])
		finally:
			return self.getPackageByIndex(packagesHasMap[name])

	def getPackage(self, name):
		packagesHasMap = self.get("PackagesHasMap")
		try:
			return self.getPackageByIndex(packagesHasMap[name])
		except Exception as e:
			raise e

	def getPackages(self):
		packagesHasIndex = self.get("PackagesHasIndex")
		packages = []
		for package in packagesHasIndex:
			packages.append(self.getPackage(package))
		return packages

	def getVersions(self):
		versions = []
		for package in self.getPackages():
			versions += package.getVersions()
		return versions

	def getDependencies(self):
		dependencies = []
		for version in self.getVersions():
			dependencies += version.getDependencies()
		return dependencies

	def getPackageSizeDistribution(self):
		packageSizeDistribution = []
		for package in self.getPackages():
			packageSizeDistribution.append(len(package.getVersions()))
		return packageSizeDistribution

	def getMostPopularVersions(self, size = None):
		mostPopularVersions = []
		popularity = {}
		for package in self.getPackages():
			for version in package.getVersions():
				popularity[version] = len(version.getOcurrences())
		popularity = sorted(popularity.items(), key = lambda x: x[1], reverse = True)
		if size:
			popularity = popularity[:size]
		for entry in popularity:
			mostPopularVersions.append(entry[0])
		return mostPopularVersions

	def getMostPopularPackages(self, size = None):
		mostPopularPackages = []
		popularity = {}
		for package in self.getPackages():
			popularity[package] = len(package.getOcurrences())
		popularity = sorted(popularity.items(), key = lambda x: x[1], reverse = True)
		if size:
			popularity = popularity[:size]
		for entry in popularity:
			mostPopularPackages.append(entry[0])
		return mostPopularPackages

	def evaluateEdges(self):
		packages = self.getPackages()
		size = len(packages)
		evaluated = 0
		for package in packages:
			for version in package.getVersions():
				for dependency in version.getDependencies():
					try:
						irregular = dependency.evaluate()
						if irregular:
							print("[" + str(evaluated) + "/" + str(size) + "]", dependency)
					except Exception as e:
						pass
				localRegularityRate = version.calculateLocalRegularityRate()
				if localRegularityRate < 1:
					print("[" + str(evaluated) + "/" + str(size) + "]", localRegularityRate, version)
			evaluated += 1

	def evaluatePackages(self):
		packages = self.getPackages()
		size = len(packages)
		evaluated = 0
		irregularPackages = []
		for package in packages:
			for packageDependency in package.getPackagesDependencies():
				if packageDependency.getLatestVersion().getDatetime():
					irregular = package.evaluate(packageDependency)
					if irregular:
						irregularPackages.append(package)
						print("[" + str(evaluated) + "/" + str(size) + "]", package, "-->", packageDependency)
						break
			evaluated += 1
		return irregularPackages

	def calculateGlobalRegularityRate(self):
		packages = self.getPackages()
		evaluated = 0
		size = len(packages)
		for package in packages:
			for version in package.getVersions():
				localRegularityRate = version.getLocalRegularityRate()
				globalRegularityRate = version.calculateGlobalRegularityRate()
				print("[" + str(evaluated) + "/" + str(size) + "]", package, "\t", "{" + str(len(package.getDependencies())) + "}", "\t", localRegularityRate, "->", globalRegularityRate)
			evaluated += 1

	def getIrregularPackages(self):
		packages = self.getPackages()
		irregularPackages = []
		for package in packages:
			if package.isIrregular():
				irregularPackages.append(package)
		return irregularPackages

	def getRegularPackages(self):
		packages = self.getPackages()
		irregularPackages = self.getIrregularPackages()
		return list(set(packages) - set(irregularPackages))

	def getIrregularVersions(self):
		packages = self.getIrregularPackages()
		irregularVersions = []
		for package in packages:
			irregularVersions += package.getIrregularVersions()
		return irregularVersions

	def getRegularVersions(self):
		versions = self.getVersions()
		irregularVersions = self.getIrregularVersions()
		return list(set(versions) - set(irregularVersions))

	def getIrregularDependencies(self):
		versions = self.getVersions()
		irregularDependencies = []
		for version in versions:
			irregularDependencies += version.getIrregularDependencies()
		return irregularDependencies

	def getRegularDependencies(self):
		dependencies = self.getDependencies()
		irregularDependencies = self.getIrregularDependencies()
		return list(set(dependencies) - set(irregularDependencies))

	def getAffectedPackages(self):
		affectedPackages = []
		packages = self.getPackages()
		for package in packages:
			if package.isAffected():
				affectedPackages.append(package)
		return affectedPackages

	def getLicenses(self):
		licenses = []
		for package in self.getPackages():
			for version in package.getVersions():
				for license in version.getLicenses():
					licenses.append(license.getName())
		licenses = set(licenses)
		licenses = list(licenses)
		return licenses

	def average(self):
		irregularPackages = 0
		irregularVersions = 0
		irregularDependencies = 0
		packages = self.getPackages()
		packagesSize = len(packages)
		versionsSize = 0
		dependenciesSize = 0
		for package in packages:
			versions = package.getVersions()
			versionsSize += len(versions)
			for version in versions:
				dependencies = version.getDependencies()
				dependenciesSize += len(dependencies)
				for dependency in dependencies:
					if dependency.isIrregular():
						irregularDependencies += 1
				if version.isIrregular():
					irregularVersions += 1
			if package.isIrregular():
				irregularPackages += 1
		print(self)
		print()
		print("irregularPackages", irregularPackages)
		print("packages", packagesSize)
		print("average", irregularPackages / packagesSize)
		print()
		print("irregularVersions", irregularVersions)
		print("versions", versionsSize)
		print("average", irregularVersions / versionsSize)
		print()
		print("irregularDependencies", irregularDependencies)
		print("dependencies", dependenciesSize)
		print("average", irregularDependencies / dependenciesSize)

	def __str__(self):
		return self.ecosystem + " at " + self.home

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<input> [<home>]")
		sys.exit(1)
	if len(sys.argv) > 2:
		home = sys.argv[2]
	else:
		home = ""
	EcosystemDataManager(sys.argv[1], home)
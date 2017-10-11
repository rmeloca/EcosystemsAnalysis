import json
import sys
import os
from .package import Package
from .group import Group

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
		self.attributes["VersionsHasGlobalRegularityMean"] = []
		self.attributes["VersionsHasLocalRegularityRate"] = []
		self.attributes["VersionsHasAuthor"] = []
		self.attributes["VersionsHasEmail"] = []
		self.attributes["VersionsHasContextSize"] = []
		self.attributes["VersionsHasDatetime"] = []
		self.attributes["VersionsHasDownloads"] = []

		self.attributes["VersionsHasOriginalLicenses"] = []
		self.attributes["VersionsHasLicenses"] = []
		self.attributes["LicensesHasGroup"] = []

		self.attributes["VersionsHasDependencies"] = []
		self.attributes["DependenciesAreIregular"] = []
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
		return [self.getPackage(package) for package in self.get("PackagesHasIndex")]

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

	def getMostPopularVersions(self, size = None):
		popularity = {version: len(version.getOcurrences()) for version in self.getVersions()}
		popularity = sorted(popularity.items(), key = lambda x: x[1], reverse = True)
		if size:
			popularity = popularity[:size]
		return [entry[0] for entry in popularity]

	def getMostPopularPackages(self, size = None):
		popularity = {package: len(package.getOcurrences()) for package in self.getPackages()}
		popularity = sorted(popularity.items(), key = lambda x: x[1], reverse = True)
		if size:
			popularity = popularity[:size]
		return [entry[0] for entry in popularity]

	def evaluateEdges(self):
		packages = self.getPackages()
		size = len(packages)
		evaluated = 0
		for package in packages:
			for version in package.getVersions():
				for dependency in version.getDependencies():
					try:
						iregular = dependency.evaluate()
						if iregular:
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
		iregularPackages = []
		for package in packages:
			for packageDependency in package.getPackagesDependencies():
				if packageDependency.getLatestVersion().getDatetime():
					iregular = package.evaluate(packageDependency)
					if iregular:
						iregularPackages.append(package)
						print("[" + str(evaluated) + "/" + str(size) + "]", package, "-->", packageDependency)
						break
			evaluated += 1
		return iregularPackages

	def calculateGlobalRegularityRate(self):
		packages = self.getPackages()
		evaluated = 0
		size = len(packages)
		for package in packages:
			for version in package.getVersions():
				localRegularityRate = version.getLocalRegularityRate()
				globalRegularityRate = version.calculateGlobalRegularityRate()
				if globalRegularityRate < 1:
					print("[" + str(evaluated) + "/" + str(size) + "]", version, "\t", "{" + str(len(version.getDependencies())) + "}", "\t", localRegularityRate, "->", globalRegularityRate)
			evaluated += 1

	def calculateGlobalRegularityMean(self):
		packages = self.getPackages()
		evaluated = 0
		size = len(packages)
		for package in packages:
			for version in package.getVersions():
				localRegularityRate = version.getLocalRegularityRate()
				globalRegularityMean = version.calculateGlobalRegularityMean()
				if globalRegularityMean < 1:
					print("[" + str(evaluated) + "/" + str(size) + "]", version, "\t", "{" + str(len(version.getDependencies())) + "}", "\t", localRegularityRate, "->", globalRegularityMean)
			evaluated += 1

	def calculateParentsSize(self, versionIndex, start = True):
		if start:
			self.visited = []
		elif versionIndex in self.visited:
			return 0
		else:
			self.visited.append(versionIndex)
		versionsHasContextSize = self.get("VersionsHasContextSize")
		if versionsHasContextSize[versionIndex]:
			return versionsHasContextSize[versionIndex]
		versionsHasOcurrences = self.get("VersionsHasOcurrences")
		parentsIndexes = versionsHasOcurrences[versionIndex]
		parentsSize = len(parentsIndexes)
		for parentIndex in parentsIndexes:
			parentsSize += self.calculateParentsSize(parentIndex, False)
		versionsHasContextSize[versionIndex] = parentsSize
		return parentsSize

	def calculateContextSize(self):
		versionsHasOcurrences = self.get("VersionsHasOcurrences")
		size = len(versionsHasOcurrences)
		for i in range(len(versionsHasOcurrences)):
			contextSize = self.calculateParentsSize(i)
			print("[" + str(i) + "/" + str(size) + "]", contextSize)

	def calculateGlobalRegularityMetrics(self):
		packages = self.getPackages()
		evaluated = 0
		size = len(packages)
		for package in packages:
			for version in package.getVersions():
				localRegularityRate = version.getLocalRegularityRate()
				globalRegularityRate = version.calculateGlobalRegularityRate()
				globalRegularityMean = version.calculateGlobalRegularityMean()
				if globalRegularityRate < 1:
					print("[" + str(evaluated) + "/" + str(size) + "]", version, "\t", "{" + str(len(version.getDependencies())) + "}", "\t", localRegularityRate, "->", globalRegularityRate, "<-", globalRegularityMean)
			evaluated += 1

	def getIregularPackages(self):
		return [package for package in self.getPackages() if package.isIregular()]

	def getRegularPackages(self):
		packages = self.getPackages()
		iregularPackages = self.getIregularPackages()
		return list(set(packages) - set(iregularPackages))

	def getIregularVersions(self):
		packages = self.getIregularPackages()
		iregularVersions = []
		for package in packages:
			iregularVersions += package.getIregularVersions()
		return iregularVersions

	def getRegularVersions(self):
		versions = self.getVersions()
		iregularVersions = self.getIregularVersions()
		return list(set(versions) - set(iregularVersions))

	def getIregularDependencies(self):
		iregularDependencies = []
		for version in self.getVersions():
			iregularDependencies += version.getIregularDependencies()
		return iregularDependencies

	def getRegularDependencies(self):
		dependencies = self.getDependencies()
		iregularDependencies = self.getIregularDependencies()
		return list(set(dependencies) - set(iregularDependencies))

	def getAffectedPackages(self):
		return [package for package in self.getPackages() if package.isAffected()]

	def getLicenses(self):
		versionsHasLicenses = self.get("VersionsHasLicenses")
		licenses = [license for version in versionsHasLicenses for license in version]
		licenses = set(licenses)
		licenses = list(licenses)
		return licenses
	
	def getMostPopularLicenses(self, size = None):
		distribution = {}
		versionsHasLicenses = self.get("VersionsHasLicenses")
		for version in versionsHasLicenses:
			for license in version:
				try:
					distribution[license] += 1
				except Exception as e:
					distribution[license] = 1
		mostPopularLicenses = sorted(distribution.items(), key=lambda x: x[1], reverse = True)
		if size:
			mostPopularLicenses = mostPopularLicenses[:size]
		return mostPopularLicenses

	def proportion(self):
		iregularPackages = 0
		affectedPackages = 0
		iregularVersions = 0
		affectedVersions = 0
		iregularDependencies = 0
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
					if dependency.isIregular():
						iregularDependencies += 1
				if version.isIregular():
					iregularVersions += 1
				if version.isAffected():
					affectedVersions += 1
			if package.isIregular():
				iregularPackages += 1
			if package.isAffected():
				affectedPackages += 1
		print(self)
		print()
		print("packages", packagesSize)
		print("iregularPackages", iregularPackages)
		print("proportion", iregularPackages / packagesSize)
		print("affectedPackages", affectedPackages)
		print("proportion", affectedPackages / packagesSize)
		print()
		print("versions", versionsSize)
		print("iregularVersions", iregularVersions)
		print("proportion", iregularVersions / versionsSize)
		print("affectedVersions", affectedVersions)
		print("proportion", affectedVersions / versionsSize)
		print()
		print("dependencies", dependenciesSize)
		print("iregularDependencies", iregularDependencies)
		print("proportion", iregularDependencies / dependenciesSize)

	def groupsProportion(self):
		versionsHasLicenses = self.get("LicensesHasGroup")
		versionsHasDatetime = self.get("VersionsHasDatetime")
		distribution = {}
		distribution["-1"] = 0
		for i in range(len(versionsHasLicenses)):
			version = versionsHasLicenses[i]
			datetime = versionsHasDatetime[i]
			if not datetime:
				continue
			if not version:
				distribution["-1"] += 1
			for group in version:
				try:
					distribution[group] += 1
				except Exception as e:
					distribution[group] = 1
		return distribution

	def licensesProportion(self):
		versionsHasLicenses = self.get("VersionsHasLicenses")
		versionsHasDatetime = self.get("VersionsHasDatetime")
		distribution = {}
		for i in range(len(versionsHasLicenses)):
			version = versionsHasLicenses[i]
			datetime = versionsHasDatetime[i]
			if not datetime:
				continue
			size = len(version)
			try:
				distribution[size] += 1
			except Exception as e:
				distribution[size] = 1
		return distribution

	def groupsDependencies(self):
		adjacencies = [[0 for groupTo in Group] for groupFrom in Group]
		versionsHasDependencies = self.get("VersionsHasDependencies")
		licensesHasGroup = self.get("LicensesHasGroup")
		versionsHasDatetime = self.get("VersionsHasDatetime")
		for i in range(len(versionsHasDependencies)):
			versionFrom = i
			dependencies = versionsHasDependencies[versionFrom]
			for j in range(len(dependencies)):
				versionTo = dependencies[j]
				datetime = versionsHasDatetime[versionTo]
				if not datetime:
					continue
				groupsFrom = licensesHasGroup[versionFrom]
				groupsTo = licensesHasGroup[versionTo]
				if not groupsFrom:
					if not groupsTo:
						adjacencies[Group.NONE.value][Group.NONE.value] += 1
					else:
						for groupTo in groupsTo:
							adjacencies[Group.NONE.value][groupTo] += 1
				elif not groupsTo:
					for groupFrom in groupsFrom:
						adjacencies[groupFrom][Group.NONE.value] += 1
				else:
					for groupFrom in groupsFrom:
						for groupTo in groupsTo:
							adjacencies[groupFrom][groupTo] += 1
		return adjacencies

	def groupsEvolution(self):
		adjacencies = [[0 for groupTo in Group] for groupFrom in Group]
		for package in self.getPackages():
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
					if not licensesTo:
						adjacencies[Group.NONE.value][Group.NONE.value] += 1
					else:
						for licenseTo in licensesTo:
							adjacencies[Group.NONE.value][licenseTo.getGroup().value] += 1
				elif not licensesTo:
					for licenseFrom in licensesFrom:
						adjacencies[licenseTo.getGroup().value][Group.NONE.value] += 1
				else:
					for licenseFrom in licensesFrom:
						for licenseTo in licensesTo:
							adjacencies[licenseFrom.getGroup().value][licenseTo.getGroup().value] += 1
		return adjacencies

	def getMostPopularIregularPackages(self, size = None):
		iregularPackages = [package for package in self.getMostPopularPackages() if package.isIregular()]
		if size:
			iregularPackages = iregularPackages[:size]
		return iregularPackages

	def backupLicenses(self):
		self.attributes["VersionsHasOriginalLicenses"] = self.get("VersionsHasLicenses")
		self.save("VersionsHasOriginalLicenses")

	def evaluateInLicenses(self, inLicenses):
		if not inLicenses:
			return True
		for inLicense in inLicenses:
			if inLicense.getGroup() == Group.NONE:
				return True
			if inLicense.getGroup() == Group.COPYRIGHT:
				return True
			if inLicense.getGroup() == Group.UNLISTED:
				return True
		return False

	def getName(self):
		return self.ecosystem

	def getLocalRegularityRates(self):
		return self.get("VersionsHasLocalRegularityRate")

	def getGlobalRegularityRates(self):
		return self.get("VersionsHasGlobalRegularityRate")

	def getGlobalRegularityMeans(self):
		return self.get("VersionsHasGlobalRegularityMean")

	def getLicensesPerVersion(self):
		return self.get("VersionsHasLicenses")

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
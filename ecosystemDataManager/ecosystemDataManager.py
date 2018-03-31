import json
import sys
import os
from .package import Package
from .group import Group

class EcosystemDataManager(object):
	"""
	docstring for EcosystemDataManager
	This class is responsible for managing persistence and retrieval for
	any ecosystem. It works by abstrating opening JSON files whose contain downloaded
	data.
	This class does not respond to fetch metadata nor delete them.
	'ecosystem' param is needed to inform what ecosystem to load.
	EcosystemDataManager will look for a folder named with 'ecosystem' variable
	content and if does not exists, will create the structure.
	'home' param is optional and describes folder to look for ecosystem.
	If 'home' not informed, EcosystemDataManager will for for 'ecosystem' in the same
	folder.
	At object construction packages are loaded.
	Once file is loaded into primary memory, EcosystemDataManager does not
	perform a garbage collection.
	Any modifications in the data must be explicitly persisted by calling
	EcosystemDataManager.save() or EcosystemDataManager.save(attribute).
	All Package, Version, Dependency, Ocurrence and License objects stores an index 
	"""
	def __init__(self, ecosystem, home = ""):
		super(EcosystemDataManager, self).__init__()
		self.home = home
		self.ecosystem = ecosystem
		self.initialize()
		self.reset()
		self.load("PackagesHasIndex")

	"""
	This function is internally called for creating requested 'ecosystem' if
	its folder does not exists.
	"""
	def initialize(self):
		try:
			os.makedirs(self.getPath())
		except Exception as e:
			pass

	"""
	This function is internally used for initialize/reset ecosystem attributes.
	Each attribute contains the file array JSON content that stores ecosystem attribute.
	Unused attributes are not loaded and once a attribute is loaded from file, variable
	content is never cleaned.
	"""
	def reset(self):
		self.attributes = {}
		self.attributes["PackagesHasIndex"] = []
		self.attributes["PackagesHasMap"] = {}
		self.attributes["PackagesHasVersions"] = []
		self.attributes["PackagesHasOccurrences"] = []
		self.attributes["PackagesHasTags"] = []
		self.attributes["PackagesHasRepository"] = []

		self.attributes["VersionsHasIndex"] = []
		self.attributes["VersionsHasPackage"] = []
		self.attributes["VersionsHasOccurrences"] = []
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
		self.attributes["DependenciesAreIrregular"] = []
		self.attributes["DependenciesHasDelimiter"] = []
		self.attributes["DependenciesHasRequirements"] = []

	"""
	getPath function abstracts the path and extension for an attribute
	if nor filename and extension is informed, getPath will return
	ecosystem home folder. Internal propouse.
	"""
	def getPath(self, filename = "", extension = ""):
		if extension:
			extension = "." + extension
		return os.path.join(self.home, self.ecosystem, filename + extension)

	"""
	save function is internally used to persist attribute into JSON file.
	If file does not exist, file is created.
	If 'attribute' is not informed, all loaded attributes will be persisted

	"""
	def save(self, attribute = None):
		if attribute:
			with open(self.getPath(attribute, "json"), "w") as file:
				file.write(json.dumps(self.attributes[attribute], separators=(',', ':')))
		else:
			for attribute in self.attributes:
				if self.attributes[attribute]:
					self.save(attribute)

	"""
	load function is internally used for load from disk JSON array attribute
	field. If file does not exist, it will be created.
	If 'attribute' is not informed, all attributes will be loaded.
	"""
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
	"""
	get function is used for get an attribute by loading if not loaded
	then return if already loaded.
	"""
	def get(self, attribute):
		if not self.attributes[attribute]:
			self.load(attribute)
		return self.attributes[attribute]

	"""
	getPackageByIndex is internally used to construct an Object
	"""
	def getPackageByIndex(self, index):
		if index < 0:
			raise Exception
		try:
			return Package(self, index)
		except Exception as e:
			raise e

	"""
	addPackage insert a package by name into ecosystemDataManager allocating spaces to attributes
	changes are not persisted untill commit (save) operation are explicitly invoked
	"""
	def addPackage(self, name):
		packagesHasMap = self.get("PackagesHasMap")
		try:
			packagesHasMap[name]
		except Exception as e:
			packagesHasIndex = self.get("PackagesHasIndex")
			packagesHasVersions = self.get("PackagesHasVersions")
			packagesHasOccurrences = self.get("PackagesHasOccurrences")
			packagesHasRepository = self.get("PackagesHasRepository")
			packagesHasTags = self.get("PackagesHasTags")

			packagesHasMap[name] = len(packagesHasIndex)
			packagesHasIndex.append(name)
			packagesHasVersions.append({})
			packagesHasOccurrences.append([])
			packagesHasRepository.append(None)
			packagesHasTags.append([])
		finally:
			return self.getPackageByIndex(packagesHasMap[name])

	"""
	getPackage construct a Package object from ecosystem data
	"""
	def getPackage(self, name):
		packagesHasMap = self.get("PackagesHasMap")
		try:
			return self.getPackageByIndex(packagesHasMap[name])
		except Exception as e:
			raise e

	"""
	getPackages constructs and return a list with all Package objects in the ecosystem
	"""
	def getPackages(self):
		return [self.getPackage(package) for package in self.get("PackagesHasIndex")]

	"""
	constructs and return a list with all Version objects in the ecosystem
	"""
	def getVersions(self):
		versions = []
		for package in self.getPackages():
			versions += package.getVersions()
		return versions

	"""
	returns the Version object given an package@version formed string
	"""
	def getVersion(self, version):
		split = version.split("@")
		return self.getPackage(split[0]).getVersion(split[1])

	"""
	constructs and return a list with all Dependency objects in the ecosystem
	"""
	def getDependencies(self):
		dependencies = []
		for version in self.getVersions():
			dependencies += version.getDependencies()
		return dependencies

	"""
	return an list of Versions ordered by version ocurrence length
	size can be informed to trucate the list
	"""
	def getMostPopularVersions(self, size = None):
		popularity = {version: len(version.getOccurrences()) for version in self.getVersions()}
		popularity = sorted(popularity.items(), key = lambda x: x[1], reverse = True)
		if size:
			popularity = popularity[:size]
		return [entry[0] for entry in popularity]

	"""
	return an list of Packages ordered by package ocurrence length
	size can be informed to trucate the list
	"""
	def getMostPopularPackages(self, size = None):
		popularity = {package: len(package.getOccurrences()) for package in self.getPackages()}
		popularity = sorted(popularity.items(), key = lambda x: x[1], reverse = True)
		if size:
			popularity = popularity[:size]
		return [entry[0] for entry in popularity]

	
	"""
	for each dependency, evaluate edges by analysing dependency licenses with choosen groups
	"""
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

	"""
	evaluatePackages considering package graph order. This functions does not alter attributes
	values. Istead, returns a dictionary of irregular packages. A package licenses are a set of
	the union of the set licenses of each version of the package.
	"""
	def evaluatePackages(self):
		packages = self.getPackages()
		size = len(packages)
		evaluated = 0
		irregularPackages = {}
		for package in packages:
			for packageDependency in package.getPackagesDependencies():
				if packageDependency.getLatestVersion().getDatetime():
					irregular = package.evaluate(packageDependency)
					if irregular:
						self.addDictKey(irregularPackages, package)
						print("[" + str(evaluated) + "/" + str(size) + "]", package, "-->", packageDependency)
						break
			evaluated += 1
		try:
			irregularPackages[package] /= len(package.getPackagesDependencies())
		except Exception as e:
			pass
		return irregularPackages

	"""
	This function calculates and change attributes of each GlobalRegularityRate of each version.
	GlobalRegularityRate is given by the product of LocalRegularityRate of the version (vertex)
	and GlobalRegularityRate of each dependency (adjacency).
	"""
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

	"""
	This function calculates and change attributes GlobalRegularityMean of each version.
	GlobalRegularityMean is given by the average between
	"""
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

	"""
	this function is internally used to calculate
	and stores the parents size of a given version.
	start parameter manages the recursion and avoid cycles.
	versionIndex is a int index of the version list.
	"""
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
		versionsHasOccurrences = self.get("VersionsHasOccurrences")
		parentsIndexes = versionsHasOccurrences[versionIndex]
		parentsSize = len(parentsIndexes)
		for parentIndex in parentsIndexes:
			parentsSize += self.calculateParentsSize(parentIndex, False)
		versionsHasContextSize[versionIndex] = parentsSize
		return parentsSize

	"""
	this function calculates and stores the parents size of each version
	"""
	def calculateContextSize(self):
		versionsHasOccurrences = self.get("VersionsHasOccurrences")
		size = len(versionsHasOccurrences)
		for i in range(len(versionsHasOccurrences)):
			contextSize = self.calculateParentsSize(i)
			print("[" + str(i) + "/" + str(size) + "]", contextSize)

	"""
	this function is internally used to calculate
	but not store the height of a given version.
	start parameter manages the recursion and avoid cycles.
	versionIndex is a int index of the version list.
	"""
	def calculateHeight(self, versionIndex, start = True):
		if start:
			self.visited = []
		elif versionIndex in self.visited:
			return 0
		else:
			self.visited.append(versionIndex)
		if versionIndex in self.heights.keys():
			return self.heights[versionIndex]
		versionsHasDependencies = self.get("VersionsHasDependencies")
		dependencyIndexes = versionsHasDependencies[versionIndex]
		heights = []
		for dependency in dependencyIndexes:
			if dependency in self.heights.keys():
				heights.append(self.heights[dependency])
			else:
				heights.append(self.calculateHeight(dependency, False))
		if not dependencyIndexes:
			height = 0
		else:
			height = 1 + max(heights)
		self.heights[versionIndex] = height
		return height

	"""
	this function calculates and prints the height of each version
	"""
	def calculateAllHeight(self):
		self.heights = {}
		versionsHasDependencies = self.get("VersionsHasDependencies")
		size = len(versionsHasDependencies)
		for i in range(len(versionsHasDependencies)):
			height = self.calculateHeight(i)
			print("[" + str(i) + "/" + str(size) + "]", height)

	"""
	calculates localRate, GlobalRate and GlobalMean of each version
	and stores. EcosystemDataManager.save() must be invoked.
	"""
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

	"""
	return a list of packages marked with irregular by evaluateEdges function.
	"""
	def getIrregularPackages(self):
		return [package for package in self.getPackages() if package.isIrregular()]

	"""
	returns the list of packages not marked as irregular.
	Packages that couldnt be evaluated also are returned.
	"""
	def getRegularPackages(self):
		packages = self.getPackages()
		irregularPackages = self.getIrregularPackages()
		return list(set(packages) - set(irregularPackages))

	"""
	returns the list of versions marked as irregular.
	"""
	def getIrregularVersions(self):
		packages = self.getIrregularPackages()
		irregularVersions = []
		for package in packages:
			irregularVersions += package.getIrregularVersions()
		return irregularVersions

	"""
	retuns the list of versions not marked as irregular.
	"""
	def getRegularVersions(self):
		versions = self.getVersions()
		irregularVersions = self.getIrregularVersions()
		return list(set(versions) - set(irregularVersions))

	"""
	returns the list of irregular dependencies
	"""
	def getIrregularDependencies(self):
		irregularDependencies = []
		for version in self.getVersions():
			irregularDependencies += version.getIrregularDependencies()
		return irregularDependencies

	"""
	returns the list of regular dependencies
	"""
	def getRegularDependencies(self):
		dependencies = self.getDependencies()
		irregularDependencies = self.getIrregularDependencies()
		return list(set(dependencies) - set(irregularDependencies))

	"""
	returns the list of affected packages. irregular packages are not put on the list.
	"""
	def getAffectedPackages(self):
		return [package for package in self.getPackages() if package.isAffected()]

	"""
	returns the list of distinct licenses used on the ecosystem.
	"""
	def getLicenses(self):
		versionsHasLicenses = self.get("VersionsHasLicenses")
		licenses = [license for version in versionsHasLicenses for license in version]
		licenses = set(licenses)
		licenses = list(licenses)
		return licenses
	
	"""
	returns the list of distinct licenses ordered by descending usage.
	size parameter can be informed to truncate the list.
	"""
	def getMostPopularLicenses(self, size = None):
		distribution = {group.value: {} for group in Group}
		versionsHasLicenses = self.get("VersionsHasLicenses")
		licensesHasGroup = self.get("LicensesHasGroup")
		for i in range(len(versionsHasLicenses)):
			version = versionsHasLicenses[i]
			for j in range(len(version)):
				license = version[j]
				group = licensesHasGroup[i][j]
				self.addDictKey(distribution[group], license)
		for group in distribution.keys():
			distribution[group] = sorted(distribution[group].items(), key=lambda x: x[1], reverse = True)
			if size:
				distribution[group] = distribution[group][:size]
		return distribution

	"""
	calculates and prints the proportion of irregular and affected packages and versions.
	"""
	def proportion(self):
		irregularPackages = 0
		affectedPackages = 0
		irregularVersions = 0
		affectedVersions = 0
		irregularDependencies = 0
		packages = self.getPackages()
		packagesSize = 0
		versionsSize = 0
		dependenciesSize = 0
		for package in packages:
			versions = package.getVersions()
			try:
				if not package.getFirstVersion():
					continue
			except Exception as e:
				print(package, "unable to get first version")
				continue
			packagesSize += 1
			for version in versions:
				if not version.getDatetime():
					continue
				versionsSize += 1
				dependencies = version.getDependencies()
				for dependency in dependencies:
					if not dependency.getInVersion().getDatetime():
						continue
					dependenciesSize += 1
					if dependency.isIrregular():
						irregularDependencies += 1
				if version.isIrregular():
					irregularVersions += 1
				if version.isAffected():
					affectedVersions += 1
			if package.isIrregular():
				irregularPackages += 1
			if package.isAffected():
				affectedPackages += 1
		print(self)
		print()
		print("packages", packagesSize)
		print("irregularPackages", irregularPackages)
		print("proportion", irregularPackages / packagesSize)
		print("affectedPackages", affectedPackages)
		print("proportion", affectedPackages / packagesSize)
		print()
		print("versions", versionsSize)
		print("irregularVersions", irregularVersions)
		print("proportion", irregularVersions / versionsSize)
		print("affectedVersions", affectedVersions)
		print("proportion", affectedVersions / versionsSize)
		print()
		print("dependencies", dependenciesSize)
		print("irregularDependencies", irregularDependencies)
		print("proportion", irregularDependencies / dependenciesSize)

	"""
	calculates and returns a dictionary with the occurrences of each license group
	"""
	def groupsProportion(self):
		versionsHasLicenses = self.get("LicensesHasGroup")
		versionsHasDatetime = self.get("VersionsHasDatetime")
		distribution = {}
		for i in range(len(versionsHasLicenses)):
			version = versionsHasLicenses[i]
			datetime = versionsHasDatetime[i]
			if not datetime:
				continue
			if not version:
				self.addDictKey(distribution, Group.NONE.value)
			for group in version:
				self.addDictKey(distribution, group)
		return distribution

	"""
	calculates and returns a dictionary with the distribution of the number
	of licenses per version.
	a dictionary key is the number of licenses and their value is the number
	of versions that hast this number of licenses associated.
	"""
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
			self.addDictKey(distribution, size)
		return distribution

	"""
	returns the propotion of groups of the latest version only
	"""
	def latestVersionsGroupsProportion(self):
		distribution = {}
		for package in self.getPackages():
			try:
				for license in package.getLatestVersion().getLicenses():
					self.addDictKey(distribution, license.getGroup().name)
			except Exception as e:
				pass
		return distribution

	"""
	returns an adjacency matrix that relates groups and quantifies the number
	of edges between license groups. In case of a list of licenses, a cartesian
	product are considered and quantified.
	"""
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

	"""
	returns an adjacency matrix that relates groups and quantifies the pairwise evolution
	of licenses between versions of a package. In case of a list of licenses, a cartesian
	product are considered and quantified.
	"""
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
						adjacencies[licenseFrom.getGroup().value][Group.NONE.value] += 1
				else:
					for licenseFrom in licensesFrom:
						for licenseTo in licensesTo:
							adjacencies[licenseFrom.getGroup().value][licenseTo.getGroup().value] += 1
		return adjacencies

	"""
	returns a dictionary adjacency matrix of the most frequent patterns of license groups evolution.
	size can be informed, so each adjacency dicitionary patterns will be truncated.
	"""
	def extractEvolutionPatterns(self, size = None):
		adjacencies = {groupFrom.name: {groupTo.name: {} for groupTo in Group} for groupFrom in Group}
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
				if not licensesFrom and licensesTo:
					for licenseTo in licensesTo:
						group = licenseTo.getGroup()
						self.addDictKey(adjacencies[Group.NONE.name][group.name], "none" + "->" + str(licenseTo))
				elif not licensesTo:
					for licenseFrom in licensesFrom:
						group = licenseFrom.getGroup()
						self.addDictKey(adjacencies[group.name][Group.NONE.name], str(licenseFrom) + "->" + "none")
				else:
					for licenseFrom in licensesFrom:
						for licenseTo in licensesTo:
							groupFrom = licenseFrom.getGroup()
							groupTo = licenseTo.getGroup()
							if licenseFrom == licenseTo:
								continue
							self.addDictKey(adjacencies[groupFrom.name][groupTo.name], str(licenseFrom) + "->" + str(licenseTo))
		for groupFrom in adjacencies.keys():
			for groupTo in adjacencies.keys():
				adjacencies[groupFrom][groupTo] = sorted(adjacencies[groupFrom][groupTo].items(), key=lambda x: x[1], reverse = True)
				if size:
					adjacencies[groupFrom][groupTo] = adjacencies[groupFrom][groupTo][:size]
		return adjacencies

	"""
	this function is internally used to increment dicionary key.
	if the key are not in the dictionary keys, key will be initialized.
	"""
	def addDictKey(self, dictionary, key):
		try:
			dictionary[key] += 1
		except Exception as e:
			dictionary[key] = 1
		return dictionary

	"""
	returns the most popular packages that are irregular.
	popularity is measured by getMostPopularPackages() funcition.
	"""
	def getMostPopularIrregularPackages(self, size = None):
		irregularPackages = [package for package in self.getMostPopularPackages() if package.isIrregular()]
		if size:
			irregularPackages = irregularPackages[:size]
		return irregularPackages

	"""
	clone licenses on a originalLicenses file.
	this funcition already saves data on disk.
	"""
	def backupLicenses(self):
		self.attributes["VersionsHasOriginalLicenses"] = self.get("VersionsHasLicenses")
		self.save("VersionsHasOriginalLicenses")

	"""
	this function is shared to Package.evaluate() and Dependency.evaluate() functions.
	inLicenses must be informed as a list of licenses objects and
	groups can be informed as a list of groups that gonna be threated as irregular
	dependency ones.
	"""
	def evaluateInLicenses(self, inLicenses, groups = [Group.NONE, Group.UNDEFINED, Group.UNAPPROVED, Group.MISUSED, Group.COPYRIGHT]):
		if Group.NONE in groups and not inLicenses:
			return True
		for inLicense in inLicenses:
			if inLicense.getGroup() in groups:
				return True
		return False

	"""
	returns the name of ecosystem, same as folder that contains their files.
	"""
	def getName(self):
		return self.ecosystem

	"""
	returns the LRR metric list
	"""
	def getLocalRegularityRates(self):
		return self.get("VersionsHasLocalRegularityRate")

	"""
	returns the GRR metric list
	"""
	def getGlobalRegularityRates(self):
		return self.get("VersionsHasGlobalRegularityRate")

	"""
	returns the GRM metric list
	"""
	def getGlobalRegularityMeans(self):
		return self.get("VersionsHasGlobalRegularityMean")

	"""
	returns the licenses matrix
	"""
	def getLicensesPerVersion(self):
		return self.get("VersionsHasLicenses")

	"""
	override print function
	"""
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
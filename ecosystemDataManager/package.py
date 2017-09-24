from datetime import datetime
from .version import Version

class Package(object):
	"""docstring for Package"""
	def __init__(self, ecosystemDataManager, index):
		super(Package, self).__init__()
		if not ecosystemDataManager or index == None:
			raise Exception
		self.ecosystemDataManager = ecosystemDataManager
		self.index = index

	def getIndex(self):
		return self.index

	def getEcosystemDataManager(self):
		return self.ecosystemDataManager

	def set(self, attribute, value):
		table = self.ecosystemDataManager.get(attribute)
		table[self.index] = value

	def get(self, attribute):
		table = self.ecosystemDataManager.get(attribute)
		return table[self.index]

	def getName(self):
		return self.get("PackagesHasIndex")

	def setRepository(self, repository):
		self.set("PackagesHasRepository", repository)
		return self

	def getRepository(self):
		return self.get("PackagesHasRepository")

	def setTags(self, tags):
		self.set("PackagesHasTags", tags)
		return self

	def getTags(self):
		return self.get("PackagesHasTags")

	def getVersionByIndex(self, index):
		if index < 0:
			raise Exception
		try:
			return Version(self.ecosystemDataManager, self, index)
		except Exception as e:
			raise e

	def resolve(self, strVersion):
		versions = self.getVersions()
		for version in versions:
			if version.satisfies(strVersion):
				return version
		raise Exception

	def addVersion(self, name):
		packagesHasVersions = self.ecosystemDataManager.get("PackagesHasVersions")
		try:
			packagesHasVersions[self.index][name]
		except Exception as e:
			versionsHasIndex = self.ecosystemDataManager.get("VersionsHasIndex")
			packagesHasVersions[self.index][name] = len(versionsHasIndex)
			versionsHasIndex.append(name)
			self.ecosystemDataManager.get("VersionsHasPackage").append(self.index)
			
			self.ecosystemDataManager.get("VersionsHasGlobalRegularityRate").append(None)
			self.ecosystemDataManager.get("VersionsHasGlobalRegularityMean").append(None)
			self.ecosystemDataManager.get("VersionsHasLocalRegularityRate").append(None)
			self.ecosystemDataManager.get("VersionsHasAuthor").append(None)
			self.ecosystemDataManager.get("VersionsHasEmail").append(None)
			self.ecosystemDataManager.get("VersionsHasContextSize").append(None)
			self.ecosystemDataManager.get("VersionsHasDatetime").append(None)
			self.ecosystemDataManager.get("VersionsHasDownloads").append(None)
			self.ecosystemDataManager.get("VersionsHasLicenses").append([])
			self.ecosystemDataManager.get("LicensesHasGroup").append([])
			self.ecosystemDataManager.get("VersionsHasDependencies").append([])
			self.ecosystemDataManager.get("VersionsHasOcurrences").append([])
			self.ecosystemDataManager.get("DependenciesAreIrregular").append([])
			self.ecosystemDataManager.get("DependenciesHasDelimiter").append([])
			self.ecosystemDataManager.get("DependenciesHasRequirements").append([])
		finally:
			return self.getVersion(name)

	def getVersion(self, name):
		versionsHasIndex = self.get("PackagesHasVersions")
		try:
			versionIndex = versionsHasIndex[name]
			return self.getVersionByIndex(versionIndex)
		except Exception as e:
			raise e

	def getVersions(self):
		versionsHasIndex = self.get("PackagesHasVersions")
		return [self.getVersion(version) for version in versionsHasIndex]

	def parseDate(self, strDate, convert = True):
		if not strDate:
			if convert:
				return datetime(1,1,1)
			raise Exception
		strDate = strDate.replace("-", " ")
		strDate = strDate.replace(".", " ")
		strDate = strDate.replace(":", " ")
		strDate = strDate.replace("T", " ")
		strDate = strDate.replace("Z", "")
		split = strDate.split(" ")
		split[0] = int(split[0])
		split[1] = int(split[1])
		split[2] = int(split[2])
		if len(split) > 3:
			split[3] = int(split[3])
			split[4] = int(split[4])
			split[5] = int(split[5])
			date = datetime(split[0], split[1], split[2], split[3], split[4], split[5])
		else:
			date = datetime(split[0], split[1], split[2])
		return date

	def getLatestVersion(self):
		versions = self.getVersions()
		if len(versions) == 0:
			raise Exception
		latestVersion = versions[0]
		latestDate = self.parseDate(latestVersion.getDatetime())
		for version in versions:
			versionDate = self.parseDate(version.getDatetime())
			if versionDate > latestDate:
				latestVersion = version
				latestDate = versionDate
		return latestVersion

	def getFirstVersion(self):
		versions = self.getVersions()
		if len(versions) == 0:
			raise Exception
		firstVersion = None
		firstDate = None
		for version in versions:
			try:
				firstDate = self.parseDate(version.getDatetime(), False)
				firstVersion = version
				break
			except Exception as e:
				pass
		for version in versions:
			try:
				versionDate = self.parseDate(version.getDatetime(), False)
				if versionDate < firstDate:
					firstVersion = version
					firstDate = versionDate
			except Exception as e:
				pass
		return firstVersion

	def getHistory(self):
		history = {version: self.parseDate(version.getDatetime()) for version in self.getVersions()}
		history = sorted(history.items(), key = lambda x: x[1])
		return [entry[0] for entry in history]

	def getDependencies(self, distinct = True):
		dependencies = []
		for version in self.getVersions():
			dependencies += version.getDependencies()
		if distinct:
			dependencies = set(dependencies)
			dependencies = list(dependencies)
		return dependencies
	
	def getOcurrences(self):
		ocurrences = []
		for version in self.getVersions():
			ocurrences += version.getOcurrences()
		ocurrences = set(ocurrences)
		ocurrences = list(ocurrences)
		return ocurrences

	def getDescendents(self):
		descendents = []
		for version in self.getVersions():
			descendents += version.getDescendents()
		descendents = set(descendents)
		descendents = list(descendents)
		return descendents

	def getParents(self):
		parents = []
		for version in self.getVersions():
			parents += version.getParents()
		parents = set(parents)
		parents = list(parents)
		return parents

	def getContext(self):
		context = self.getParents() + self.getDescendents()
		context = set(context)
		context = list(context)
		return context

	def getPackagesDependencies(self):
		packages = [dependency.getInVersion().getPackage() for dependency in self.getDependencies()]
		packages = set(packages)
		packages = list(packages)
		return packages

	def getPackagesOcurrences(self):
		packagesHasOcurrences = self.ecosystemDataManager.get("PackagesHasOcurrences")
		indexes = packagesHasOcurrences[self.index]
		ocurrences = [self.ecosystemDataManager.getPackageByIndex(indexes[package]) for package in indexes]
		ocurrences = set(ocurrences)
		ocurrences = list(ocurrences)
		return ocurrences
		
	def getPackagesDescendents(self):
		packages = [descendent.getPackage() for descendent in self.getDescendents()]
		packages = set(packages)
		packages = list(packages)
		return packages

	def getPackagesParents(self):
		packages = [parent.getPackage() for parent in self.getParents()]
		parents = set(parents)
		parents = list(parents)
		return packages

	def getPackagesContext(self):
		context = self.getPackagesParents() + self.getPackagesDescendents()
		context = set(context)
		context = list(context)
		return context

	def getLicenses(self):
		licenses = []
		for version in self.getVersions():
			licenses += version.getLicenses()
		licenses = set(licenses)
		licenses = list(licenses)
		return licenses

	def getLocalRegularityRates(self):
		return [version.getLocalRegularityRate() for version in self.getVersions()]

	def getMostPopularVersions(self, size = None):
		popularity = {version: len(version.getOcurrences()) for version in self.getVersions()}
		popularity = sorted(popularity.items(), key = lambda x: x[1], reverse = True)
		if size:
			popularity = popularity[:size]
		return [entry[0] for entry in popularity]

	def getFirstInsertion(self):
		return self.getFirstVersion().getDatetime()

	def evaluate(self, dependency):
		inLicenses = dependency.getLicenses()
		if inLicenses:
			irregular = False
		else:
			irregular = True
		for inLicense in inLicenses:
			if inLicense == "copyright" or inLicense == "none" or inLicense == None:
				irregular = True
				break
		return irregular

	def isIrregular(self):
		for version in self.getVersions():
			if version.isIrregular():
				return True
		return False

	def isRegular(self):
		for version in self.getVersions():
			if version.isIrregular():
				return False
		return True

	def getIrregularVersions(self):
		return [version for version in self.getVersions() if version.isIrregular()]

	def getRegularVersions(self):
		versions = self.getVersions()
		irregularVersions = self.getIrregularVersions()
		return list(set(versions) - set(irregularVersions))

	def isAffected(self):
		for version in self.getVersions():
			if version.getGlobalRegularityRate() < 1:
				return True
		return False

	def __hash__(self):
		return self.index

	def __len__(self):
		return len(self.get("PackagesHasVersions"))

	def __eq__(self, other):
		if type(other) != type(self):
			return False
		return other.getIndex() == self.getIndex()

	def __str__(self):
		return self.getName()
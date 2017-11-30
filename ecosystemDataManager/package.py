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
	"""
	This function is internally called for initialization of the class and set all attributes.
	If haven't set all requested this class cound't be initialized.
	"""
	def getIndex(self):
		return self.index
	"""
	This function is internally called to return the index itself
	"""
	def getEcosystemDataManager(self):
		return self.ecosystemDataManager
	"""
	This function is internally called to return the ecosystem data manager itself
	"""
	def set(self, attribute, value):
		table = self.ecosystemDataManager.get(attribute)
		table[self.index] = value
	"""
	This function is internally called to set table value by the requests attributes
	"""
	def get(self, attribute):
		table = self.ecosystemDataManager.get(attribute)
		return table[self.index]
	"""
	This function is internally called to return the requested attribute of this package
	"""
	def getName(self):
		return self.get("PackagesHasIndex")
	"""
	This function is internally called to return the package name itself 
	"""
	def setRepository(self, repository):
		self.set("PackagesHasRepository", repository)
		return self

	def getRepository(self):
		return self.get("PackagesHasRepository")
	"""
	This function is internally called to return the repository itself
	"""
	def setTags(self, tags):
		self.set("PackagesHasTags", tags)
		return self
	"""
	This function is internally called to set some tags
	"""
	def getTags(self):
		return self.get("PackagesHasTags")
	"""
	This function is internally called to return the tags itself
	"""
	def getVersionByIndex(self, index):
		if index < 0:
			raise Exception
		try:
			return Version(self.ecosystemDataManager, self, index)
		except Exception as e:
			raise e
	"""
	This function is internally called to return version by requested index
	"""
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
			self.ecosystemDataManager.get("DependenciesAreIregular").append([])
			self.ecosystemDataManager.get("DependenciesHasDelimiter").append([])
			self.ecosystemDataManager.get("DependenciesHasRequirements").append([])
		finally:
			return self.getVersion(name)
	"""
	This function is internally called to add a new version to this package.
	"""
	
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
		indexes = self.get("PackagesHasOcurrences")
		ocurrences = [self.ecosystemDataManager.getPackageByIndex(index) for index in indexes]
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
		packages = set(packages)
		packages = list(packages)
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
		return self.ecosystemDataManager.evaluateInLicenses(inLicenses)

	def isIregular(self):
		for version in self.getVersions():
			if version.isIregular():
				return True
		return False
	"""
	This function is internally called to return if at least one version is irregular, this
	package is irregular too.
	"""
	def isRegular(self):
		for version in self.getVersions():
			if version.isIregular():
				return False
		return True
	"""
	This function is internally called to return if any version is irregular, this
	package is regular.
	"""
	def getIregularVersions(self):
		return [version for version in self.getVersions() if version.isIregular()]
	"""
	This function is internally called to return a list of iregular versions
	"""
	def getRegularVersions(self):
		versions = self.getVersions()
		iregularVersions = self.getIregularVersions()
		return list(set(versions) - set(iregularVersions))
	"""
	This function is internally called to return a list of regular versions
	"""
	def isAffected(self):
		for version in self.getVersions():
			if version.getGlobalRegularityRate() < 1:
				return True
		return False
	"""
	This function is internally called to return if itself pakcage is affected ou not, by
	the global regularity rate.
	"""	

	def __hash__(self):
		return self.index
	"""
	This overwritten function is internally called to return the self index for hash
	"""
	def __len__(self):
		return len(self.get("PackagesHasVersions"))
	"""
	This overwritten function is internally called to return the self len by len of PackagesHasVersions
	"""
	def __eq__(self, other):
		if type(other) != type(self):
			return False
		return other.getIndex() == self.getIndex()
	"""
	This overwritten function is internally called to compare this license with other license by license Index
	"""
	def __str__(self):
		return self.getName()
	"""
	This overwritten function is internally called to return license Name
	"""
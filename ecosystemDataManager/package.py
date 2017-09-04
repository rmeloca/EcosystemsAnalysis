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

	def addVersion(self, name):
		packagesHasVersions = self.ecosystemDataManager.get("PackagesHasVersions")
		try:
			packagesHasVersions[self.index][name]
		except Exception as e:
			versionsHasIndex = self.ecosystemDataManager.get("VersionsHasIndex")
			versionsHasPackage = self.ecosystemDataManager.get("VersionsHasPackage")
			versionsHasOcurrences = self.ecosystemDataManager.get("VersionsHasOcurrences")
			versionsHasGlobalRegularityRate = self.ecosystemDataManager.get("VersionsHasGlobalRegularityRate")
			versionsHasLocalRegularityRate = self.ecosystemDataManager.get("VersionsHasLocalRegularityRate")
			versionsHasAuthors = self.ecosystemDataManager.get("VersionsHasAuthors")
			versionsHasContextSize = self.ecosystemDataManager.get("VersionsHasContextSize")
			versionsHasDatetime = self.ecosystemDataManager.get("VersionsHasDatetime")
			versionsHasDownloads = self.ecosystemDataManager.get("VersionsHasDownloads")
			versionsHasLinesOfCode = self.ecosystemDataManager.get("VersionsHasLinesOfCode")
			versionsHasMaintainers = self.ecosystemDataManager.get("VersionsHasMaintainers")
			
			versionsHasLicenses = self.ecosystemDataManager.get("VersionsHasLicenses")
			licensesHasGroup = self.ecosystemDataManager.get("LicensesHasGroup")
			
			versionsHasDependencies = self.ecosystemDataManager.get("VersionsHasDependencies")
			dependenciesAreIrregular = self.ecosystemDataManager.get("DependenciesAreIrregular")
			dependenciesHasDelimiter = self.ecosystemDataManager.get("DependenciesHasDelimiter")
			dependenciesHasRequirements = self.ecosystemDataManager.get("DependenciesHasRequirements")
			
			packagesHasVersions[self.index][name] = len(versionsHasIndex)
			versionsHasIndex.append(name)
			versionsHasPackage.append(self.index)
			versionsHasOcurrences.append([])
			versionsHasGlobalRegularityRate.append(None)
			versionsHasLocalRegularityRate.append(None)
			versionsHasAuthors.append({})
			versionsHasContextSize.append(None)
			versionsHasDatetime.append(None)
			versionsHasDownloads.append(None)
			versionsHasLinesOfCode.append(None)
			versionsHasMaintainers.append([])

			versionsHasLicenses.append([])
			licensesHasGroup.append([])
			
			versionsHasDependencies.append([])
			dependenciesAreIrregular.append([])
			dependenciesHasDelimiter.append([])
			dependenciesHasRequirements.append([])
		finally:
			return self.getVersionByIndex(packagesHasVersions[self.index][name])

	def getVersions(self):
		packagesHasVersions = self.ecosystemDataManager.get("PackagesHasVersions")
		versionsHasIndex = packagesHasVersions[self.index]
		versions = []
		for version in versionsHasIndex:
			versions.append(self.getVersionByIndex(versionsHasIndex[version]))
		return versions

	def getVersion(self, name):
		packagesHasVersions = self.ecosystemDataManager.get("PackagesHasVersions")
		try:
			versionIndex = packagesHasVersions[self.index][name]
			return self.getVersionByIndex(versionIndex)
		except Exception as e:
			raise e

	def getLastestVersion(self):
		versions = self.getVersions()
		if len(versions) == 0:
			raise Exception
		latestVersion = versions[0]
		for version in versions:
			if version.getDatetime() > latestVersion.getDatetime():
				latestVersion = version
		return latestVersion

	def getDependencies(self):
		versions = self.getVersions()
		dependencies = []
		for version in versions:
			dependencies += version.getDependencies()
		dependencies = set(dependencies)
		dependencies = list(dependencies)
		return dependencies
	
	def getOcurrences(self):
		versions = self.getVersions()
		ocurrences = []
		for version in versions:
			ocurrences += version.getOcurrences()
		ocurrences = set(ocurrences)
		ocurrences = list(ocurrences)
		return ocurrences

	def getDescendents(self):
		versions = self.getVersions()
		descendents = []
		for version in versions:
			descendents += version.getDescendents()
		descendents = set(descendents)
		descendents = list(descendents)
		return descendents

	def getParents(self):
		versions = self.getVersions()
		parents = []
		for version in versions:
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
		dependencies = self.getDependencies()
		packages = []
		for dependency in dependencies:
			packages.append(dependency.getInVersion().getPackage())
		packages = set(packages)
		packages = list(packages)
		return packages

	def getPackagesOcurrences(self):
		packagesHasOcurrences = self.ecosystemDataManager.get("PackagesHasOcurrences")
		indexes = packagesHasOcurrences[self.index]
		ocurrences = []
		for package in indexes:
			ocurrences.append(self.ecosystemDataManager.getPackageByIndex(indexes[package]))
		ocurrences = set(ocurrences)
		ocurrences = list(ocurrences)
		return ocurrences
		
	def getPackagesDescendents(self):
		descendents = self.getDescendents()
		packages = []
		for descendent in descendents:
			packages.append(descendent.getPackage())
		descendents = set(descendents)
		descendents = list(descendents)
		return packages

	def getPackagesParents(self):
		parents = self.getParents()
		packages = []
		for parent in parents:
			packages.append(parent.getPackage())
		parents = set(parents)
		parents = list(parents)
		return packages

	def getPackagesContext(self):
		context = self.getPackagesParents() + self.getPackagesDescendents()
		context = set(context)
		context = list(context)
		return context

	def getLocalRegularityRate(self):
		localRegularityRate = []
		for version in self.getVersions():
			localRegularityRate.append(version.getLocalRegularityRate())
		return localRegularityRate

	def __eq__(self, other):
		if type(other) != type(self):
			return False
		return other.getIndex() == self.getIndex()

	def __str__(self):
		return self.getName()
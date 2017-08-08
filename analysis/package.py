from version import Version

class Package(object):
	"""docstring for Package"""
	def __init__(self, ecossystemDataManager, index):
		super(Package, self).__init__()
		if not ecossystemDataManager or index == None:
			raise Exception
		self.ecossystemDataManager = ecossystemDataManager
		self.index = index

	def getName(self):
		return self.ecossystemDataManager.packagesHasIndex[self.index]

	def getRepository(self):
		packagesHasRepository = self.ecossystemDataManager.getPackagesHasRepository()
		return packagesHasRepository[self.index]

	def getTags(self):
		packagesHasTags =  self.ecossystemDataManager.getPackagesHasTags()
		return packagesHasTags[self.index]

	def getVersionByIndex(self, index):
		if index < 0:
			raise Exception
		try:
			return Version(self.ecossystemDataManager, self, index)
		except Exception as e:
			raise e

	def getVersions(self):
		packagesHasVersions = self.ecossystemDataManager.getPackagesHasVersions()
		versionsHasIndex = packagesHasVersions[self.index]
		versions = []
		for version in versionsHasIndex:
			versions.append(self.getVersionByIndex(versionsHasIndex[version]))
		return versions

	def getVersion(self, name):
		packagesHasVersions = self.ecossystemDataManager.getPackagesHasVersions()
		try:
			versionIndex = packagesHasVersions[self.index][name]
			return self.getVersionByIndex(versionIndex)
		except Exception as e:
			raise e

	def addVersion(self, name):
		packagesHasVersions = self.ecossystemDataManager.getPackagesHasVersions()
		try:
			packagesHasVersions[self.index][name]
		except Exception as e:
			versionsHasIndex = self.ecossystemDataManager.getVersionsHasIndex()
			versionsHasPackage = self.ecossystemDataManager.getVersionsHasPackage()
			versionsHasOcurrences = self.ecossystemDataManager.getVersionsHasOcurrences()
			versionsHasGlobalRegularityRate = self.ecossystemDataManager.getVersionsHasGlobalRegularityRate()
			versionsHasLocalRegularityRate = self.ecossystemDataManager.getVersionsHasLocalRegularityRate()
			versionsHasDependencies = self.ecossystemDataManager.getVersionsHasDependencies()
			versionsHasLicenses = self.ecossystemDataManager.getVersionsHasLicenses()
			dependenciesAreIrregular = self.ecossystemDataManager.getDependenciesAreIrregular()
			packagesHasVersions[self.index][name] = len(versionsHasIndex)
			versionsHasIndex.append(name)
			versionsHasPackage.append(self.index)
			versionsHasOcurrences.append([])
			versionsHasGlobalRegularityRate.append(None)
			versionsHasLocalRegularityRate.append(None)
			versionsHasDependencies.append([])
			versionsHasLicenses.append([])
			dependenciesAreIrregular.append([])
		finally:
			return self.getVersionByIndex(packagesHasVersions[self.index][name])

	def getOcurrences(self):
		packagesHasOcurrences = self.ecossystemDataManager.getPackagesHasOcurrences()
		indexes = packagesHasOcurrences[self.index]
		ocurrences = []
		for package in indexes:
			ocurrences.append(self.ecossystemDataManager.getPackageByIndex(indexes[package]))
		return ocurrences
from dependency import Dependency
from ocurrence import Ocurrence

class Version(object):
	"""docstring for Version"""
	def __init__(self, ecossystemDataManager, package, index):
		super(Version, self).__init__()
		if not ecossystemDataManager or index == None:
			raise Exception
		self.ecossystemDataManager = ecossystemDataManager
		if not package:
			versionsHasPackage = self.ecossystemDataManager.getVersionsHasPackage()
			package = self.ecossystemDataManager.getPackageByIndex(versionsHasPackage[index])
		self.package = package
		self.index = index

	def getIndex(self):
		return self.index

	def getPackage(self):
		return self.package

	def getName(self):
		versionsHasIndex = self.ecossystemDataManager.getVersionsHasIndex()
		return versionsHasIndex[self.index]

	def getDependencies(self):
		versionsHasDependencies =  self.ecossystemDataManager.getVersionsHasDependencies()
		indexes = versionsHasDependencies[self.index]
		dependencies = []
		for dependency in indexes:
			inVersion = Version(self.ecossystemDataManager, None, dependency)
			dependencies.append(Dependency(self.ecossystemDataManager, self, inVersion, dependency))
		return dependencies

	def getOcurrences(self):
		versionsHasOcurrences =  self.ecossystemDataManager.getVersionsHasOcurrences()
		indexes = versionsHasOcurrences[self.index]
		ocurrences = []
		for ocurrence in indexes:
			ocurrences.append(Ocurrence(self, Version(self.ecossystemDataManager, None, ocurrence)))
		return ocurrences

	def getDatetime(self):
		versionsHasDatetime = self.ecossystemDataManager.getVersionsHasDatetime()
		return versionsHasDatetime[self.index]

	def getDownloads(self):
		versionsHasDownloads = self.ecossystemDataManager.getVersionsHasDownloads()
		return versionsHasDownloads[self.index]

	def getLinesOfCode(self):
		versionsHasLinesOfCode = self.ecossystemDataManager.getVersionsHasLinesOfCode()
		return versionsHasLinesOfCode[self.index]

	def getLocalRegularityRate(self):
		versionsHasLocalRegularityRate = self.ecossystemDataManager.getVersionsHasLocalRegularityRate()
		return versionsHasLocalRegularityRate[self.index]

	def getGlobalRegularityRate(self):
		versionsHasGlobalRegularityRate = self.ecossystemDataManager.getVersionsHasGlobalRegularityRate()
		return versionsHasGlobalRegularityRate[self.index]

	def getContext(self):
		return self.getDescendents() + self.getParents()

	def getDescendents(self):
		dependencies = self.getDependencies()
		descendents = []
		for dependency in dependencies:
			descendents.append(dependency.getInVersion())
			descendents += dependency.getInVersion().getDescendents()
		return descendents

	def getParents(self):
		ocurrences = self.getOcurrences()
		parents = []
		for ocurrence in ocurrences:
			parents.append(ocurrence.getInVersion())
			parents += ocurrence.getInVersion().getParents()
		return parents

	def getLicenses(self):
		versionsHasLicenses = self.ecossystemDataManager.getVersionsHasLicenses()
		return versionsHasLicenses[self.index]

	def addDependency(self, version):
		versionsHasDependencies = self.ecossystemDataManager.getVersionsHasDependencies()
		if version.getIndex() in versionsHasDependencies[self.index]:
			dependencyIndex = versionsHasDependencies[self.index].indexOf(version.getIndex())
		else:
			versionsHasOcurrences = self.ecossystemDataManager.getVersionsHasOcurrences()
			dependencyIndex = len(versionsHasDependencies[self.index])
			versionsHasDependencies[self.index].append(version.getIndex())
			versionsHasOcurrences[version.getIndex()].append(self.getIndex())
		packagesHasOcurrences = self.ecossystemDataManager.getPackagesHasOcurrences()
		if self.package.getIndex() in packagesHasOcurrences[version.getPackage().getIndex()]:
			pass
		else:
			packagesHasOcurrences[version.getPackage().getIndex()].append(self.package.getIndex())	
		return Dependency(self.ecossystemDataManager, self, version, dependencyIndex)
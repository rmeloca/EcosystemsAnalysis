from .dependency import Dependency
from .ocurrence import Ocurrence

class Version(object):
	"""docstring for Version"""
	def __init__(self, ecosystemDataManager, package, index):
		super(Version, self).__init__()
		if not ecosystemDataManager or index == None:
			raise Exception
		self.ecosystemDataManager = ecosystemDataManager
		if not package:
			versionsHasPackage = self.ecosystemDataManager.get("VersionsHasPackage")
			package = self.ecosystemDataManager.getPackageByIndex(versionsHasPackage[index])
		self.package = package
		self.index = index

	def getIndex(self):
		return self.index

	def getPackage(self):
		return self.package

	def getName(self):
		versionsHasIndex = self.ecosystemDataManager.get("VersionsHasIndex")
		return versionsHasIndex[self.index]

	def getDatetime(self):
		versionsHasDatetime = self.ecosystemDataManager.get("VersionsHasDatetime")
		return versionsHasDatetime[self.index]

	def getDownloads(self):
		versionsHasDownloads = self.ecosystemDataManager.get("VersionsHasDownloads")
		return versionsHasDownloads[self.index]

	def getLinesOfCode(self):
		versionsHasLinesOfCode = self.ecosystemDataManager.get("VersionsHasLinesOfCode")
		return versionsHasLinesOfCode[self.index]

	def getLocalRegularityRate(self):
		versionsHasLocalRegularityRate = self.ecosystemDataManager.get("VersionsHasLocalRegularityRate")
		return versionsHasLocalRegularityRate[self.index]

	def getGlobalRegularityRate(self):
		versionsHasGlobalRegularityRate = self.ecosystemDataManager.get("VersionsHasGlobalRegularityRate")
		return versionsHasGlobalRegularityRate[self.index]

	def getLicenses(self):
		versionsHasLicenses = self.ecosystemDataManager.get("VersionsHasLicenses")
		return versionsHasLicenses[self.index]

	def addDependency(self, version):
		versionsHasDependencies = self.ecosystemDataManager.get("VersionsHasDependencies")
		if version.getIndex() in versionsHasDependencies[self.index]:
			dependencyIndex = versionsHasDependencies[self.index].index(version.getIndex())
		else:
			versionsHasOcurrences = self.ecosystemDataManager.get("VersionsHasOcurrences")
			dependencyIndex = len(versionsHasDependencies[self.index])
			versionsHasDependencies[self.index].append(version.getIndex())
			versionsHasOcurrences[version.getIndex()].append(self.getIndex())
		packagesHasOcurrences = self.ecosystemDataManager.get("PackagesHasOcurrences")
		if self.package.getIndex() in packagesHasOcurrences[version.getPackage().getIndex()]:
			pass
		else:
			packagesHasOcurrences[version.getPackage().getIndex()].append(self.package.getIndex())
		return Dependency(self.ecosystemDataManager, self, version, dependencyIndex)

	def getDependencies(self):
		versionsHasDependencies =  self.ecosystemDataManager.get("VersionsHasDependencies")
		indexes = versionsHasDependencies[self.index]
		dependencies = []
		for dependency in indexes:
			inVersion = Version(self.ecosystemDataManager, None, dependency)
			dependencies.append(Dependency(self.ecosystemDataManager, self, inVersion, dependency))
		return dependencies

	def getOcurrences(self):
		versionsHasOcurrences =  self.ecosystemDataManager.get("VersionsHasOcurrences")
		indexes = versionsHasOcurrences[self.index]
		ocurrences = []
		for ocurrence in indexes:
			ocurrences.append(Ocurrence(self, Version(self.ecosystemDataManager, None, ocurrence)))
		return ocurrences

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

	def getContext(self):
		return self.getParents() + self.getDescendents()

	def equals(self, other):
		if type(other) != type(self):
			return False
		return other.getIndex() == self.getIndex()
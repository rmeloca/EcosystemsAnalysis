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

	def set(self, attribute, value):
		table = self.ecosystemDataManager.get(attribute)
		table[self.index] = value

	def get(self, attribute):
		table = self.ecosystemDataManager.get(attribute)
		return table[self.index]

	def getName(self):
		return self.get("VersionsHasIndex")

	def setDatetime(self, datetime):
		self.set("VersionsHasDatetime", datetime)

	def getDatetime(self):
		return self.get("VersionsHasDatetime")

	def setDownloads(self, downloads):
		self.set("VersionsHasDownloads", downloads)

	def getDownloads(self):
		return self.get("VersionsHasDownloads")

	def setLinesOfCode(self, linesOfCode):
		self.set("VersionsHasLinesOfCode", linesOfCode)

	def getLinesOfCode(self):
		return self.get("VersionsHasLinesOfCode")

	def setLocalRegularityRate(self, localRegularityRate):
		self.set("VersionsHasLocalRegularityRate", localRegularityRate)

	def getLocalRegularityRate(self):
		return self.get("VersionsHasLocalRegularityRate")

	def setGlobalRegularityRate(self, globalRegularityRate):
		self.set("VersionsHasGlobalRegularityRate", globalRegularityRate)

	def getGlobalRegularityRate(self):
		return self.get("VersionsHasGlobalRegularityRate")

	def addLicense(self, license):
		versionsHasLicenses = self.get("VersionsHasLicenses")
		if license not in versionsHasLicenses:
			versionsHasLicenses.append(license)

	def setLicenses(self, licenses):
		self.set("VersionsHasLicenses", licenses)

	def getLicenses(self):
		return self.get("VersionsHasLicenses")

	def addAuthor(self, email, name):
		self.get("VersionsHasAuthors")[email] = name

	def setAuthors(self, authors):
		self.set("VersionsHasAuthors", authors)

	def getAuthors(self):
		return self.get("VersionsHasAuthors")

	def addDependency(self, version):
		versionsHasDependencies = self.ecosystemDataManager.get("VersionsHasDependencies")
		if version.getIndex() in versionsHasDependencies[self.index]:
			dependencyIndex = versionsHasDependencies[self.index].index(version.getIndex())
		else:
			versionsHasOcurrences = self.ecosystemDataManager.get("VersionsHasOcurrences")
			dependenciesHasDelimiter = self.ecosystemDataManager.get("DependenciesHasDelimiter")
			dependenciesHasRequirements = self.ecosystemDataManager.get("DependenciesHasRequirements")
			dependenciesAreIrregular = self.ecosystemDataManager.get("DependenciesAreIrregular")
			
			dependencyIndex = len(versionsHasDependencies[self.index])
			versionsHasDependencies[self.index].append(version.getIndex())
			versionsHasOcurrences[version.getIndex()].append(self.getIndex())
			dependenciesHasDelimiter[self.index].append(None)
			dependenciesHasRequirements[self.index].append(None)
			dependenciesAreIrregular[self.index].append(None)
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
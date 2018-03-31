from .dependency import Dependency
from .occurrence import Occurrence
from .license import License

class Version(object):
	"""
	This function is internally called for initialization of the class and set all attributes.
	If haven't set ecosystemDataManager or index requested this class cound't be initialized.
	"""
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
		return self

	def get(self, attribute):
		table = self.ecosystemDataManager.get(attribute)
		return table[self.index]

	"""
	This function is internally called to return the version name itself 
	"""
	def getName(self):
		return self.get("VersionsHasIndex")

	def setDatetime(self, datetime):
		self.set("VersionsHasDatetime", datetime)
		return self

	def getDatetime(self):
		return self.get("VersionsHasDatetime")

	def setDownloads(self, downloads):
		self.set("VersionsHasDownloads", downloads)
		return self

	def getDownloads(self):
		return self.get("VersionsHasDownloads")

	def getLocalRegularityRate(self):
		return self.get("VersionsHasLocalRegularityRate")

	def getGlobalRegularityRate(self, start = True):
		if start:
			self.ecosystemDataManager.visited = []
		globalRegularityRate = self.get("VersionsHasGlobalRegularityRate")
		if not globalRegularityRate:
			if self in self.ecosystemDataManager.visited:
				return 1
			else:
				globalRegularityRate = self.calculateGlobalRegularityRate(False)
		return globalRegularityRate

	def getGlobalRegularityMean(self, start = True):
		if start:
			self.ecosystemDataManager.visited = []
		globalRegularityMean = self.get("VersionsHasGlobalRegularityMean")
		if not globalRegularityMean:
			if self in self.ecosystemDataManager.visited:
				return 1
			else:
				globalRegularityMean = self.calculateGlobalRegularityMean(False)
		return globalRegularityMean

	def getContextSize(self):
		contextSize = self.get("VersionsHasContextSize")
		if not contextSize:
			contextSize = self.calculateContextSize()
		return contextSize

	def getLicenseByIndex(self, index):
		if index < 0:
			raise Exception
		try:
			return License(self.ecosystemDataManager, self, index)
		except Exception as e:
			raise e

	def addLicense(self, license):
		versionsHasLicenses = self.get("VersionsHasLicenses")
		licensesHasGroup = self.get("LicensesHasGroup")
		if license in versionsHasLicenses:
			licenseIndex = versionsHasLicenses.index(license)
		else:
			licenseIndex = len(versionsHasLicenses)
			licensesHasGroup.append(None)
			versionsHasLicenses.append(license)
		return self.getLicenseByIndex(licenseIndex)

	def setLicenses(self, licenses):
		self.set("VersionsHasLicenses", [])
		self.set("LicensesHasGroup", [])
		return [self.addLicense(license) for license in licenses]

	def getLicenses(self):
		versionsHasLicenses = self.get("VersionsHasLicenses")
		licenses = []
		for license in versionsHasLicenses:
			licenses.append(self.getLicenseByIndex(len(licenses)))
		return licenses

	def getOriginalLicenses(self):
		return self.get("VersionsHasOriginalLicenses")

	def setAuthor(self, author):
		self.set("VersionsHasAuthor", author)
		return self

	def getAuthor(self):
		return self.get("VersionsHasAuthor")

	def setEmail(self, email):
		self.set("VersionsHasEmail", email)
		return self

	def getEmail(self):
		return self.get("VersionsHasEmail")

	def satisfies(self, strVersion):
		name = self.getName()
		for i in range(len(name)):
			if strVersion[i] == "x":
				return True
			elif strVersion[i] != name[i]:
				return False
		return True

	def addDependency(self, version):
		versionsHasDependencies = self.ecosystemDataManager.get("VersionsHasDependencies")
		if version.getIndex() in versionsHasDependencies[self.index]:
			dependencyIndex = versionsHasDependencies[self.index].index(version.getIndex())
		else:
			versionsHasOccurrences = self.ecosystemDataManager.get("VersionsHasOccurrences")
			dependenciesHasDelimiter = self.ecosystemDataManager.get("DependenciesHasDelimiter")
			dependenciesHasRequirements = self.ecosystemDataManager.get("DependenciesHasRequirements")
			dependenciesAreIrregular = self.ecosystemDataManager.get("DependenciesAreIrregular")

			dependencyIndex = len(versionsHasDependencies[self.index])
			versionsHasDependencies[self.index].append(version.getIndex())
			versionsHasOccurrences[version.getIndex()].append(self.getIndex())
			dependenciesHasDelimiter[self.index].append(None)
			dependenciesHasRequirements[self.index].append(None)
			dependenciesAreIrregular[self.index].append(None)
		packagesHasOccurrences = self.ecosystemDataManager.get("PackagesHasOccurrences")
		if self.package.getIndex() in packagesHasOccurrences[version.getPackage().getIndex()]:
			pass
		else:
			packagesHasOccurrences[version.getPackage().getIndex()].append(self.package.getIndex())
		return Dependency(self.ecosystemDataManager, self, version, dependencyIndex)

	def manageRecursion(self, start):
		if start:
			self.ecosystemDataManager.visited = []
		elif self in self.ecosystemDataManager.visited:
			return False
		else:
			self.ecosystemDataManager.visited.append(self)
		return True

	def getDependencies(self, recursive = False, start = True):
		if recursive:
			goOn = self.manageRecursion(start)
			if not goOn:
				return []
		versionsHasDependencies =  self.ecosystemDataManager.get("VersionsHasDependencies")
		indexes = versionsHasDependencies[self.index]
		dependencies = []
		for dependency in indexes:
			inVersion = Version(self.ecosystemDataManager, None, dependency)
			dependencies.append(Dependency(self.ecosystemDataManager, self, inVersion, len(dependencies)))
		if recursive:
			descendents = []
			descendents += dependencies
			for dependency in dependencies:
				descendents += dependency.getInVersion().getDependencies(True, False)
			return descendents
		return dependencies

	def getOccurrences(self, recursive = False, start = True):
		if recursive:
			goOn = self.manageRecursion(start)
			if not goOn:
				return []
		versionsHasOccurrences =  self.ecosystemDataManager.get("VersionsHasOccurrences")
		indexes = versionsHasOccurrences[self.index]
		occurrences =  [Occurrence(self.ecosystemDataManager, self, Version(self.ecosystemDataManager, None, occurrence)) for occurrence in indexes]
		if recursive:
			parents = []
			parents += occurrences
			for occurrence in occurrences:
				parents += occurrence.getInVersion().getOccurrences(True, False)
			return parents
		return occurrences

	def getDescendents(self, start = True):
		goOn = self.manageRecursion(start)
		if not goOn:
			return []
		dependencies = self.getDependencies()
		descendents = []
		for dependency in dependencies:
			descendents.append(dependency.getInVersion())
			descendents += dependency.getInVersion().getDescendents(False)
		descendents = set(descendents)
		descendents = list(descendents)
		return descendents

	def getParents(self, start = True):
		goOn = self.manageRecursion(start)
		if not goOn:
			return []
		occurrences = self.getOccurrences()
		parents = []
		for occurrence in occurrences:
			parents.append(occurrence.getInVersion())
			parents += occurrence.getInVersion().getParents(False)
		parents = set(parents)
		parents = list(parents)
		return parents

	def getContext(self):
		context = self.getParents() + self.getDescendents()
		context = set(context)
		context = list(context)
		return context

	def getHeight(self, start = True):
		goOn = self.manageRecursion(start)
		if not goOn:
			return 0
		dependencies =  self.getDependencies()
		if not dependencies:
			return 0
		try:
			self.ecosystemDataManager.heights
		except Exception as e:
			self.ecosystemDataManager.heights = {}
		heights = []
		for dependency in dependencies:
			if dependency in self.ecosystemDataManager.heights.keys():
				heights.append(self.ecosystemDataManager.heights[dependency])
			else:
				heights.append(dependency.getInVersion().getHeight(False))
		height = 1 + max(heights)
		self.ecosystemDataManager.heights[self] = height
		return height

	def isIrregular(self):
		dependencies = self.getDependencies()
		for dependency in dependencies:
			if dependency.isIrregular():
				return True
		return False

	def isRegular(self):
		dependencies = self.getDependencies()
		for dependency in dependencies:
			if dependency.isIrregular():
				return False
		return True

	def isAffected(self):
		if self.getGlobalRegularityRate() < 1:
			return True
		return False

	def getIrregularDependencies(self):
		return [dependency for dependency in self.getDependencies() if dependency.isIrregular()]

	def getRegularDependencies(self):
		dependencies = self.getDependencies()
		irregularDependencies = self.getIrregularDependencies()
		return list(set(dependencies) - set(irregularDependencies))

	def calculateLocalRegularityRate(self):
		try:
			localRegularityRate = len(self.getRegularDependencies()) / len(self.getDependencies())
		except Exception as e:
			localRegularityRate = 1
		self.set("VersionsHasLocalRegularityRate", localRegularityRate)
		return localRegularityRate

	def calculateGlobalRegularityRate(self, start = True):
		if start:
			self.ecosystemDataManager.visited = []
		self.ecosystemDataManager.visited.append(self)
		globalRegularityRate = self.getLocalRegularityRate()
		dependencies = self.getDependencies()
		for dependency in dependencies:
			globalRegularityRate *= dependency.getInVersion().getGlobalRegularityRate(False)
		self.set("VersionsHasGlobalRegularityRate", globalRegularityRate)
		return globalRegularityRate

	def calculateContextSize(self):
		contextSize = len(self.getParents())
		self.set("VersionsHasContextSize", contextSize)
		return contextSize

	def calculateGlobalRegularityMean(self, start = True):
		if start:
			self.ecosystemDataManager.visited = []
		self.ecosystemDataManager.visited.append(self)
		globalRegularityMean = self.getLocalRegularityRate()
		dependencies = self.getDependencies()
		for dependency in dependencies:
			globalRegularityMean += dependency.getInVersion().getGlobalRegularityMean(False)
		globalRegularityMean /= len(dependencies) + 1
		self.set("VersionsHasGlobalRegularityMean", globalRegularityMean)
		return globalRegularityMean

	"""
	This overwritten function is internally called to return the self index for hash
	"""
	def __hash__(self):
		return self.index

	"""
	This overwritten function is internally called to compare this license with other license by license Index
	"""
	def __eq__(self, other):
		if type(other) != type(self):
			return False
		return other.getIndex() == self.getIndex()

	"""
	This overwritten function is internally called to return license Name
	"""
	def __str__(self):
		return self.getPackage().getName() + "@" + str(self.getName())
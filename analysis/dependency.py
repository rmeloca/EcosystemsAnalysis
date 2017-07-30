class Dependency(object):
	"""docstring for Dependency"""
	def __init__(self, ecossystemDataManager, outVersion, inVersion, index):
		super(Dependency, self).__init__()
		if not ecossystemDataManager or not outVersion or not index:
			raise Exception
		self.ecossystemDataManager = ecossystemDataManager
		self.outVersion = outVersion
		if not inVersion:
			versionsHasDependencies = self.ecossystemDataManager.getVersionsHasDependencies()
			inVersionIndex = versionsHasDependencies[index]
			inVersion = Version(self.ecossystemDataManager, None, inVersionIndex)
		self.inVersion = inVersion
		self.index = index

	def getOutVersion(self):
		return self.outVersion

	def getInVersion(self):
		return self.inVersion

	def getDelimiter(self):
		dependenciesHasDelimiter = self.ecossystemDataManager.getDependenciesHasDelimiter()
		return dependenciesHasDelimiter[self.outVersion.getIndex()][self.index]

	def isIrregular(self):
		dependenciesAreIrregular = self.ecossystemDataManager.getDependenciesAreIrregular()
		return dependenciesAreIrregular[self.outVersion.getIndex()][self.index]

	def isRegular(self):
		return not self.isIrregular()
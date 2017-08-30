class Dependency(object):
	"""docstring for Dependency"""
	def __init__(self, ecosystemDataManager, outVersion, inVersion, index):
		super(Dependency, self).__init__()
		if not ecosystemDataManager or not outVersion or not inVersion or not index:
			raise Exception
		self.ecosystemDataManager = ecosystemDataManager
		self.outVersion = outVersion
		self.inVersion = inVersion
		self.index = index

	def getIndex(self):
		return self.index

	def getOutVersion(self):
		return self.outVersion

	def getInVersion(self):
		return self.inVersion

	def getDelimiter(self):
		dependenciesHasDelimiter = self.ecosystemDataManager.get("DependenciesHasDelimiter")
		return dependenciesHasDelimiter[self.outVersion.getIndex()][self.index]

	def isIrregular(self):
		dependenciesAreIrregular = self.ecosystemDataManager.get("DependenciesAreIrregular")
		return dependenciesAreIrregular[self.outVersion.getIndex()][self.index]

	def isRegular(self):
		return not self.isIrregular()

	def equals(self, other):
		if type(other) != type(self):
			return False
		return other.getIndex() == self.getIndex()
class Dependency(object):
	"""docstring for Dependency"""
	def __init__(self, ecosystemDataManager, outVersion, inVersion, index):
		super(Dependency, self).__init__()
		if not ecosystemDataManager or not outVersion or not inVersion or index == None:
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

	def set(self, attribute, value):
		table = self.ecosystemDataManager.get(attribute)
		table[self.outVersion.getIndex()][self.index] = value

	def get(self, attribute):
		table = self.ecosystemDataManager.get(attribute)
		return table[self.outVersion.getIndex()][self.index]

	def setDelimiter(self, delimiter):
		self.set("DependenciesHasDelimiter", delimiter)

	def getDelimiter(self):
		return self.get("DependenciesHasDelimiter")

	def setIrregular(self, irregular):
		self.set("DependenciesAreIrregular", irregular)

	def isIrregular(self):
		return self.get("DependenciesAreIrregular")

	def setRequirements(self, delimiter):
		self.set("DependenciesHasRequirements", delimiter)

	def getRequirements(self):
		return self.get("DependenciesHasRequirements")

	def isRegular(self):
		return not self.isIrregular()

	def equals(self, other):
		if type(other) != type(self):
			return False
		return other.getIndex() == self.getIndex()
class Dependency(object):
	"""docstring for Dependency"""
	def __init__(self, ecosystemDataManager, outVersion, inVersion, index):
		super(Dependency, self).__init__()
		if not ecosystemDataManager or not outVersion or not inVersion:
			raise Exception
		self.ecosystemDataManager = ecosystemDataManager
		self.outVersion = outVersion
		self.inVersion = inVersion
		self.index = index
		if index == None:
			self.index = self.ecosystemDataManager.get("VersionsHasDependencies")[self.outVersion.getIndex()].index(self.inVersion.getIndex())

	def getIndex(self):
		return self.index

	def getOutVersion(self):
		return self.outVersion

	def getInVersion(self):
		return self.inVersion

	def set(self, attribute, value):
		table = self.ecosystemDataManager.get(attribute)
		table[self.outVersion.getIndex()][self.index] = value
		return self

	def get(self, attribute):
		table = self.ecosystemDataManager.get(attribute)
		return table[self.outVersion.getIndex()][self.index]

	def setDelimiter(self, delimiter):
		self.set("DependenciesHasDelimiter", delimiter)
		return self

	def getDelimiter(self):
		return self.get("DependenciesHasDelimiter")

	def setRequirements(self, requirements):
		self.set("DependenciesHasRequirements", requirements)
		return self

	def getRequirements(self):
		return self.get("DependenciesHasRequirements")

	def isIrregular(self):
		return self.get("DependenciesAreIrregular") == True

	def isRegular(self):
		return self.get("DependenciesAreIrregular") == False

	def evaluate(self):
		if not self.inVersion.getDatetime():
			irregular = None
			self.set("DependenciesAreIrregular", irregular)
			raise Exception
		inLicenses = self.inVersion.getLicenses()
		irregular = self.ecosystemDataManager.evaluateInLicenses(inLicenses)
		self.set("DependenciesAreIrregular", irregular)
		return irregular

	def __hash__(self):
		return self.index

	def __eq__(self, other):
		if type(other) != type(self):
			return False
		return other.getIndex() == self.getIndex()

	def __str__(self):
		return self.outVersion.__str__() + " --> " + self.inVersion.__str__()
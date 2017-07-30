class License(object):
	"""docstring for License"""
	def __init__(self, ecossystemDataManager, version, index):
		super(License, self).__init__()
		self.ecossystemDataManager = ecossystemDataManager
		self.version = version
		self.index = index

	def getName(self):
		versionsHasLicenses = self.ecossystemDataManager.getVersionsHasLicenses()
		return versionsHasLicenses[self.version.getIndex()][self.index]

	def getGroup(self):
		licensesHasGroup = self.ecossystemDataManager.getLicensesHasGroup()
		return Group(licensesHasGroup[self.version.getIndex()][self.index])

	def setGroup(self, group):
		licensesHasGroup = self.ecossystemDataManager.getLicensesHasGroup()
		licensesHasGroup[self.version.getIndex()][self.index] = group.value
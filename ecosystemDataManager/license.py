class License(object):
	"""docstring for License"""
	def __init__(self, ecosystemDataManager, version, index):
		super(License, self).__init__()
		self.ecosystemDataManager = ecosystemDataManager
		self.version = version
		self.index = index

	def getName(self):
		versionsHasLicenses = self.ecosystemDataManager.get("VersionsHasLicenses")
		return versionsHasLicenses[self.version.getIndex()][self.index]

	def getGroup(self):
		licensesHasGroup = self.ecosystemDataManager.get("LicensesHasGroup")
		return Group(licensesHasGroup[self.version.getIndex()][self.index])

	def setGroup(self, group):
		licensesHasGroup = self.ecosystemDataManager.get("LicensesHasGroup")
		licensesHasGroup[self.version.getIndex()][self.index] = group.value
		return self
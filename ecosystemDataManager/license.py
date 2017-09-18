from .group import Group

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

	def __hash__(self):
		return self.index

	def __eq__(self, other):
		if type(other) == str:
			return self.getName() == other
		elif type(other) != type(self):
			return False
		return self.getName() == other.getName()

	def __str__(self):
		return self.getName()
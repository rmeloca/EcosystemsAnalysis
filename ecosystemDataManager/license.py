from .group import Group

class License(object):
	"""
	This class is responsible for managing all attributes of lincese class, 
	like it self ecosystemDataManager, version and index
	"""
	def __init__(self, ecosystemDataManager, version, index):
		super(License, self).__init__()
		self.ecosystemDataManager = ecosystemDataManager
		self.version = version
		self.index = index
	"""
	This function is internally called for initialization of the class and set all attributes
	"""

	def getName(self):
		versionsHasLicenses = self.ecosystemDataManager.get("VersionsHasLicenses")
		return versionsHasLicenses[self.version.getIndex()][self.index]
	"""
	This function is internally called to return the license name itself 
	"""

	def getGroup(self):
		licensesHasGroup = self.ecosystemDataManager.get("LicensesHasGroup")
		return Group(licensesHasGroup[self.version.getIndex()][self.index])
	"""
	This function is internally called to return the license group itself
	"""

	def setGroup(self, group):
		licensesHasGroup = self.ecosystemDataManager.get("LicensesHasGroup")
		licensesHasGroup[self.version.getIndex()][self.index] = group.value
		return self
	"""
	This function is internally called to set the new group
	"""
	def __hash__(self):
		return self.index
	"""
	This overwritten function is internally called to return the self index for hash
	"""
	def __eq__(self, other):
		if type(other) == str:
			return self.getName() == other
		elif type(other) != type(self):
			return False
		return self.getName() == other.getName()
	"""
	This overwritten function is internally called to compare this license with other license by license Name
	"""
	def __str__(self):
		return self.getName()
	"""
	This overwritten function is internally called to return license Name
	"""
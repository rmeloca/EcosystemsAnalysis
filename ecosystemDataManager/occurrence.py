from .dependency import Dependency

class Occurrence(object):
	"""docstring for Occurrence"""
	def __init__(self, ecosystemDataManager, outVersion, inVersion):
		super(Occurrence, self).__init__()
		if not ecosystemDataManager or not outVersion or not inVersion:
			raise Exception
		self.ecosystemDataManager = ecosystemDataManager
		self.outVersion = outVersion
		self.inVersion = inVersion

	def getOutVersion(self):
		return self.outVersion

	def getInVersion(self):
		return self.inVersion

	def getDependency(self):
		return Dependency(self.ecosystemDataManager, self.inVersion, self.outVersion, None)

	def __str__(self):
		return self.outVersion.__str__() + " --> " + self.inVersion.__str__()
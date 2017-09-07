class Ocurrence(object):
	"""docstring for Ocurrence"""
	def __init__(self, outVersion, inVersion):
		super(Ocurrence, self).__init__()
		if not outVersion or not inVersion:
			raise Exception
		self.outVersion = outVersion
		self.inVersion = inVersion

	def getOutVersion(self):
		return self.outVersion

	def getInVersion(self):
		return self.inVersion

	def __str__(self):
		return self.outVersion.__str__() + " --> " + self.inVersion.__str__()
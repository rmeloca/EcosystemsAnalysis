from .dependency import Dependency

class Ocurrence(object):
	"""
	This class is responsible for represent an edge of a graph, and that edge is the 
	occurrence of a dependency
	"""
	def __init__(self, ecosystemDataManager, outVersion, inVersion):
		super(Ocurrence, self).__init__()
		if not ecosystemDataManager or not outVersion or not inVersion:
			raise Exception
		self.ecosystemDataManager = ecosystemDataManager
		self.outVersion = outVersion
		self.inVersion = inVersion
	"""
	This function is internally called for initialization of the class and set all attributes.
	If haven't set all requested this class cound't be initialized.
	"""
	def getOutVersion(self):
		return self.outVersion
	"""
	This function is internally called to return the vertex that the edge has its origin
	"""
	def getInVersion(self):
		return self.inVersion
	"""
	This function is internally called to return the vertex that this vertex points
	"""
	def getDependency(self):
		return Dependency(self.ecosystemDataManager, self.inVersion, self.outVersion, None)
	"""
	This function is internally called to return the inverse of this ocurrence. That is, a dependency edge.
	"""
	def __str__(self):
		return self.outVersion.__str__() + " --> " + self.inVersion.__str__()
	"""
	This overwritten function is internally called to return license Name
	"""
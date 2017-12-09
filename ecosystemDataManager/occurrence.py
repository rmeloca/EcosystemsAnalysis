from .dependency import Dependency

class Occurrence(object):
	"""
	This class is responsible for represent an edge of a graph, and that edge is the 
	occurrence of a dependency
	Constructor is internally called for initialization of the class and set all attributes.
	If haven't set all requested this class cound't be initialized.
	"""
	def __init__(self, ecosystemDataManager, outVersion, inVersion):
		super(Occurrence, self).__init__()
		if not ecosystemDataManager or not outVersion or not inVersion:
			raise Exception
		self.ecosystemDataManager = ecosystemDataManager
		self.outVersion = outVersion
		self.inVersion = inVersion

	"""
	This function is internally called to return the vertex that the edge has its origin
	"""
	def getOutVersion(self):
		return self.outVersion

	"""
	This function is internally called to return the vertex that this vertex points
	"""
	def getInVersion(self):
		return self.inVersion

	"""
	This function is internally called to return the inverse of this ocurrence. That is, a dependency edge.
	"""
	def getDependency(self):
		return Dependency(self.ecosystemDataManager, self.inVersion, self.outVersion, None)

	"""
	This overwritten function is internally called to return license Name
	"""
	def __str__(self):
		return self.outVersion.__str__() + " --> " + self.inVersion.__str__()
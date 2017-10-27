from enum import Enum

class Group(Enum):
	"""docstring for Group"""
	UNDEFINED = 0
	COPYRIGHT = 1
	MISUSED = 2
	FILE = 3
	UNAPPROVED = 4
	KNOWN = 5
	NONE = 6
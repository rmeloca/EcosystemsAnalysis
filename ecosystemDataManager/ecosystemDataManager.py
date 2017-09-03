import json
import sys
import os
from .package import Package

class EcosystemDataManager(object):
	"""docstring for EcosystemDataManager"""
	def __init__(self, ecosystem, home = ""):
		super(EcosystemDataManager, self).__init__()
		if home != "":
			self.home = home
		self.ecosystem = ecosystem
		self.initialize()
		self.reset()
		self.load("PackagesHasIndex")

	def initialize(self):
		try:
			os.makedirs(self.getPath())
		except Exception as e:
			pass

	def reset(self):
		self.attributes = {}
		self.attributes["PackagesHasIndex"] = []
		self.attributes["PackagesHasMap"] = {}
		self.attributes["PackagesHasVersions"] = []
		self.attributes["PackagesHasOcurrences"] = []
		self.attributes["PackagesHasTags"] = []
		self.attributes["PackagesHasRepository"] = []

		self.attributes["VersionsHasIndex"] = []
		self.attributes["VersionsHasPackage"] = []
		self.attributes["VersionsHasOcurrences"] = []
		self.attributes["VersionsHasGlobalRegularityRate"] = []
		self.attributes["VersionsHasLocalRegularityRate"] = []
		self.attributes["VersionsHasAuthors"] = []
		self.attributes["VersionsHasContextSize"] = []
		self.attributes["VersionsHasDatetime"] = []
		self.attributes["VersionsHasDownloads"] = []
		self.attributes["VersionsHasLinesOfCode"] = []
		self.attributes["VersionsHasMaintainers"] = []

		self.attributes["VersionsHasLicenses"] = []
		self.attributes["LicensesHasGroup"] = []

		self.attributes["VersionsHasDependencies"] = []
		self.attributes["DependenciesAreIrregular"] = []
		self.attributes["DependenciesHasDelimiter"] = []
		self.attributes["DependenciesHasRequirements"] = []

	def getPath(self, filename = "", extension = ""):
		if extension:
			extension = "." + extension
		return os.path.join(self.home, self.ecosystem, filename + extension)

	def save(self, attribute = None):
		if attribute:
			with open(self.getPath(attribute, "json"), "w") as file:
				file.write(json.dumps(self.attributes[attribute], separators=(',', ':')))
		else:
			for attribute in self.attributes:
				if self.attributes[attribute]:
					self.save(attribute)

	def load(self, attribute = None):
		if attribute:
			try:
				with open(self.getPath(attribute, "json")) as file:
					self.attributes[attribute] = json.load(file)
			except Exception as e:
				self.save(attribute)
		else:
			for attribute in self.attributes:
				self.load(attribute)

	def get(self, attribute):
		if not self.attributes[attribute]:
			self.load(attribute)
		return self.attributes[attribute]

	def getPackageByIndex(self, index):
		if index < 0:
			raise Exception
		try:
			return Package(self, index)
		except Exception as e:
			raise e

	def addPackage(self, name):
		packagesHasMap = self.get("PackagesHasMap")
		try:
			packagesHasMap[name]
		except Exception as e:
			packagesHasIndex = self.get("PackagesHasIndex")
			packagesHasVersions = self.get("PackagesHasVersions")
			packagesHasOcurrences = self.get("PackagesHasOcurrences")
			packagesHasRepository = self.get("PackagesHasRepository")
			packagesHasTags = self.get("PackagesHasTags")

			packagesHasMap[name] = len(packagesHasIndex)
			packagesHasIndex.append(name)
			packagesHasVersions.append({})
			packagesHasOcurrences.append([])
			packagesHasRepository.append(None)
			packagesHasTags.append([])
		finally:
			return self.getPackageByIndex(packagesHasMap[name])

	def getPackages(self):
		packagesHasIndex = self.get("PackagesHasIndex")
		packages = []
		for package in packagesHasIndex:
			packages.append(self.getPackage(package))
		return packages

	def getPackage(self, name):
		packagesHasMap = self.get("PackagesHasMap")
		try:
			return self.getPackageByIndex(packagesHasMap[name])
		except Exception as e:
			raise e

	def getPackageSizeDistribution(self):
		packageSizeDistribution = []
		for package in self.getPackages():
			packageSizeDistribution.append(len(package.getVersions()))
		return packageSizeDistribution

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<input> [<home>]")
		sys.exit(1)
    if len(sys.argv) > 2:
        home = sys.argv[2]
    else:
        home = ""
	EcosystemDataManager(sys.argv[1], home)
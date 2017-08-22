import json
import sys
import os
from package import Package

class EcossystemDataManager(object):
	"""docstring for EcossystemDataManager"""
	def __init__(self, ecossystem):
		super(EcossystemDataManager, self).__init__()
		self.ecossystem = ecossystem
		self.resetData()
		self.loadPackagesHasIndex()

	def resetData(self):
		self.packagesHasIndex = []
		self.packagesHasMap = {}
		self.packagesHasVersions = []
		self.packagesHasOcurrences = []
		self.versionsHasIndex = []
		self.versionsHasPackage = []
		self.versionsHasOcurrences = []
		self.versionsHasGlobalRegularityRate = []
		self.versionsHasLocalRegularityRate = []
		self.versionsHasDependencies = []
		self.dependenciesAreIrregular = []
		self.versionsHasLicenses = []

	def getPath(self, filename):
		return os.path.join("..", self.ecossystem, "data", filename)

	def loadPackagesHasIndex(self):
		try:
			with open(self.getPath("packagesHasIndex.json")) as packagesHasIndexFile:
				self.packagesHasIndex = json.load(packagesHasIndexFile)
		except Exception as e:
			self.savePackagesHasIndex()

	def loadPackagesHasMap(self):
		try:
			with open(self.getPath("packagesHasMap.json")) as packagesHasMapFile:
				self.packagesHasMap = json.load(packagesHasMapFile)
		except Exception as e:
			self.savePackagesHasMap()

	def loadPackagesHasVersions(self):
		try:
			with open(self.getPath("packagesHasVersions.json")) as packagesHasVersionsFile:
				self.packagesHasVersions = json.load(packagesHasVersionsFile)
		except Exception as e:
			self.savePackagesHasVersions()

	def loadPackagesHasOcurrences(self):
		try:
			with open(self.getPath("packagesHasOcurrences.json")) as packagesHasOcurrencesFile:
				self.packagesHasOcurrences = json.load(packagesHasOcurrencesFile)
		except Exception as e:
			self.savePackagesHasOcurrences()

	def loadVersionsHasIndex(self):
		try:
			with open(self.getPath("versionsHasIndex.json")) as versionsHasIndexFile:
				self.versionsHasIndex = json.load(versionsHasIndexFile)
		except Exception as e:
			self.saveVersionsHasIndex()

	def loadVersionsHasPackage(self):
		try:
			with open(self.getPath("versionsHasPackage.json")) as versionsHasPackageFile:
				self.versionsHasPackage = json.load(versionsHasPackageFile)
		except Exception as e:
			self.saveVersionsHasPackage()

	def loadVersionsHasOcurrences(self):
		try:
			with open(self.getPath("versionsHasOcurrences.json")) as versionsHasOcurrencesFile:
				self.versionsHasOcurrences = json.load(versionsHasOcurrencesFile)
		except Exception as e:
			self.saveVersionsHasOcurrences()

	def loadVersionsHasGlobalRegularityRate(self):
		try:
			with open(self.getPath("versionsHasGlobalRegularityRate.json")) as versionsHasGlobalRegularityRateFile:
				self.versionsHasGlobalRegularityRate = json.load(versionsHasGlobalRegularityRateFile)
		except Exception as e:
			self.saveVersionsHasGlobalRegularityRate()

	def loadVersionsHasLocalRegularityRate(self):
		try:
			with open(self.getPath("versionsHasLocalRegularityRate.json")) as versionsHasLocalRegularityRateFile:
				self.versionsHasLocalRegularityRate = json.load(versionsHasLocalRegularityRateFile)
		except Exception as e:
			self.saveVersionsHasLocalRegularityRate()

	def loadVersionsHasDependencies(self):
		try:
			with open(self.getPath("versionsHasDependencies.json")) as versionsHasDependenciesFile:
				self.versionsHasDependencies = json.load(versionsHasDependenciesFile)
		except Exception as e:
			self.saveVersionsHasDependencies()

	def loadDependenciesAreIrregular(self):
		try:
			with open(self.getPath("dependenciesAreIrregular.json")) as dependenciesAreIrregularFile:
				self.dependenciesAreIrregular = json.load(dependenciesAreIrregularFile)
		except Exception as e:
			self.saveDependenciesAreIrregular()

	def loadVersionsHasLicenses(self):
		try:
			with open(self.getPath("versionsHasLicenses.json")) as versionsHasLicensesFile:
				self.versionsHasLicenses = json.load(versionsHasLicensesFile)
		except Exception as e:
			self.saveVersionsHasLicenses()

	def getPackagesHasIndex(self):
		if not self.packagesHasIndex:
			self.loadPackagesHasIndex()
		return self.packagesHasIndex

	def getPackagesHasMap(self):
		if not self.packagesHasMap:
			self.loadPackagesHasMap()
		return self.packagesHasMap

	def getPackagesHasVersions(self):
		if not self.packagesHasVersions:
			self.loadPackagesHasVersions()
		return self.packagesHasVersions

	def getPackagesHasOcurrences(self):
		if not self.packagesHasOcurrences:
			self.loadPackagesHasOcurrences()
		return self.packagesHasOcurrences

	def getVersionsHasIndex(self):
		if not self.versionsHasIndex:
			self.loadVersionsHasIndex()
		return self.versionsHasIndex

	def getVersionsHasPackage(self):
		if not self.versionsHasPackage:
			self.loadVersionsHasPackage()
		return self.versionsHasPackage

	def getVersionsHasOcurrences(self):
		if not self.versionsHasOcurrences:
			self.loadVersionsHasOcurrences()
		return self.versionsHasOcurrences

	def getVersionsHasGlobalRegularityRate(self):
		if not self.versionsHasGlobalRegularityRate:
			self.loadVersionsHasGlobalRegularityRate()
		return self.versionsHasGlobalRegularityRate

	def getVersionsHasLocalRegularityRate(self):
		if not self.versionsHasLocalRegularityRate:
			self.loadVersionsHasLocalRegularityRate()
		return self.versionsHasLocalRegularityRate

	def getVersionsHasDependencies(self):
		if not self.versionsHasDependencies:
			self.loadVersionsHasDependencies()
		return self.versionsHasDependencies

	def getDependenciesAreIrregular(self):
		if not self.dependenciesAreIrregular:
			self.loadDependenciesAreIrregular()
		return self.dependenciesAreIrregular

	def getVersionsHasLicenses(self):
		if not self.versionsHasLicenses:
			self.loadVersionsHasLicenses()
		return self.versionsHasLicenses

	def savePackagesHasIndex(self):
		with open(self.getPath("packagesHasIndex.json"), "w") as packagesHasIndexFile:
			packagesHasIndexFile.write(json.dumps(self.packagesHasIndex, separators=(',', ':')))

	def savePackagesHasMap(self):
		with open(self.getPath("packagesHasMap.json"), "w") as packagesHasMapFile:
			packagesHasMapFile.write(json.dumps(self.packagesHasMap, separators=(',', ':')))

	def savePackagesHasVersions(self):
		with open(self.getPath("packagesHasVersions.json"), "w") as packagesHasVersionsFile:
			packagesHasVersionsFile.write(json.dumps(self.packagesHasVersions, separators=(',', ':')))

	def savePackagesHasOcurrences(self):
		with open(self.getPath("packagesHasOcurrences.json"), "w") as packagesHasOcurrencesFile:
			packagesHasOcurrencesFile.write(json.dumps(self.packagesHasOcurrences, separators=(',', ':')))

	def saveVersionsHasIndex(self):
		with open(self.getPath("versionsHasIndex.json"), "w") as versionsHasIndexFile:
			versionsHasIndexFile.write(json.dumps(self.versionsHasIndex, separators=(',', ':')))

	def saveVersionsHasPackage(self):
		with open(self.getPath("versionsHasPackage.json"), "w") as versionsHasPackageFile:
			versionsHasPackageFile.write(json.dumps(self.versionsHasPackage, separators=(',', ':')))

	def saveVersionsHasOcurrences(self):
		with open(self.getPath("versionsHasOcurrences.json"), "w") as versionsHasOcurrencesFile:
			versionsHasOcurrencesFile.write(json.dumps(self.versionsHasOcurrences, separators=(',', ':')))

	def saveVersionsHasGlobalRegularityRate(self):
		with open(self.getPath("versionsHasGlobalRegularityRate.json"), "w") as versionsHasGlobalRegularityRateFile:
			versionsHasGlobalRegularityRateFile.write(json.dumps(self.versionsHasGlobalRegularityRate, separators=(',', ':')))

	def saveVersionsHasLocalRegularityRate(self):
		with open(self.getPath("versionsHasLocalRegularityRate.json"), "w") as versionsHasLocalRegularityRateFile:
			versionsHasLocalRegularityRateFile.write(json.dumps(self.versionsHasLocalRegularityRate, separators=(',', ':')))

	def saveVersionsHasDependencies(self):
		with open(self.getPath("versionsHasDependencies.json"), "w") as versionsHasDependenciesFile:
			versionsHasDependenciesFile.write(json.dumps(self.versionsHasDependencies, separators=(',', ':')))

	def saveDependenciesAreIrregular(self):
		with open(self.getPath("dependenciesAreIrregular.json"), "w") as dependenciesAreIrregularFile:
			dependenciesAreIrregularFile.write(json.dumps(self.dependenciesAreIrregular, separators=(',', ':')))

	def saveVersionsHasLicenses(self):
		with open(self.getPath("versionsHasLicenses.json"), "w") as versionsHasLicensesFile:
			versionsHasLicensesFile.write(json.dumps(self.versionsHasLicenses, separators=(',', ':')))

	def save(self):
		if self.packagesHasIndex:
			self.savePackagesHasIndex()
		if self.packagesHasMap:
			self.savePackagesHasMap()
		if self.packagesHasVersions:
			self.savePackagesHasVersions()
		if self.packagesHasOcurrences:
			self.savePackagesHasOcurrences()
		if self.versionsHasIndex:
			self.saveVersionsHasIndex()
		if self.versionsHasPackage:
			self.saveVersionsHasPackage()
		if self.versionsHasOcurrences:
			self.saveVersionsHasOcurrences()
		if self.versionsHasGlobalRegularityRate:
			self.saveVersionsHasGlobalRegularityRate()
		if self.versionsHasLocalRegularityRate:
			self.saveVersionsHasLocalRegularityRate()
		if self.versionsHasDependencies:
			self.saveVersionsHasDependencies()
		if self.dependenciesAreIrregular:
			self.saveDependenciesAreIrregular()
		if self.versionsHasLicenses:
			self.saveVersionsHasLicenses()

	def load(self):
		self.loadPackagesHasIndex()
		self.loadPackagesHasMap()
		self.loadPackagesHasVersions()
		self.loadPackagesHasOcurrences()
		self.loadVersionsHasIndex()
		self.loadVersionsHasPackage()
		self.loadVersionsHasOcurrences()
		self.loadVersionsHasGlobalRegularityRate()
		self.loadVersionsHasLocalRegularityRate()
		self.loadVersionsHasDependencies()
		self.loadDependenciesAreIrregular()
		self.loadVersionsHasLicenses()

	def getPackageByIndex(self, index):
		if index < 0:
			raise Exception
		try:
			return Package(self, index)
		except Exception as e:
			raise e

	def getPackage(self, name):
		packagesHasMap = self.getPackagesHasMap()
		try:
			return self.getPackageByIndex(packagesHasMap[name])
		except Exception as e:
			raise e

	def getPackages(self):
		packages = []
		packagesHasMap = self.getPackagesHasMap()
		for package in packagesHasMap:
			packages.append(self.getPackageByIndex(packagesHasMap[package]))
		return packages

	def addPackage(self, name):
		packagesHasMap = self.getPackagesHasMap()
		try:
			return self.getPackageByIndex(packagesHasMap[name])
		except Exception as e:
			packagesHasIndex = self.getPackagesHasIndex()
			packagesHasVersions = self.getPackagesHasVersions()
			packagesHasOcurrences = self.getPackagesHasOcurrences()
			packagesHasMap[name] = len(packagesHasIndex)
			packagesHasIndex.append(name)
			packagesHasVersions.append({})
			packagesHasOcurrences.append([])
			return self.getPackageByIndex(packagesHasMap[name])

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<input>")
		sys.exit(1)
	EcossystemDataManager(sys.argv[1])
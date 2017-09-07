import sys
import os
import requests
import json
from bs4 import BeautifulSoup
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

RUBYGEMS_PACKAGES_HAS_VERSIONS = {}
NPM_VISITED_PACKAGES = []

def getContent(url):
	request = requests.get(url)
	if request.status_code != 200:
		raise Exception
	return request.text

def getJson(url):
	return json.loads(getContent(url))

def fetchNpm(package):
	if package in NPM_VISITED_PACKAGES:
		return
	NPM_VISITED_PACKAGES.append(package)
	ecosystemDataManager = package.getEcosystemDataManager()
	registry = 'https://registry.npmjs.org'
	metadata = getJson(os.path.join(registry, package.getName()))
	try:
		package.setTags(metadata["keywords"])
	except Exception as e:
		print(package.getName(), "no keyworks", e)
	try:
		package.setRepository(metadata["repository"]["url"])
	except Exception as e:
		print(package.getName(), "no repository", e)
	for metadataVersion in metadata["versions"]:
		version = package.addVersion(metadataVersion)
		licenses = []
		try:
			for license in metadata["versions"][metadataVersion]["licenses"]:
				licenses.append(license["type"])
		except Exception as e:
			print(package.getName() + "@" + metadataVersion, "no licenses", e)
		try:
			licenses.append(metadata["versions"][metadataVersion]["license"])
		except Exception as e:
			print(package.getName() + "@" + metadataVersion, "no license", e)
		version.setLicenses(licenses)
		version.setDatetime(metadata["time"][metadataVersion])
		try:
			version.setAuthor(metadata["versions"][metadataVersion]["author"]["name"])
		except Exception as e:
			print(package.getName() + "@" + metadataVersion, "no author", e)
		try:
			version.setEmail(metadata["versions"][metadataVersion]["author"]["email"])
		except Exception as e:
			print(package.getName() + "@" + metadataVersion, "no email", e)
		for metadataDependency in metadata["versions"][metadataVersion]["dependencies"]:
			try:
				key = metadataDependency
				value = metadata["versions"][metadataVersion]["dependencies"][metadataDependency]
				requirements = value
				value = value.split(" ")[0]
				value = value.replace("x", "0")
				delimiter = None
				if value[1] == "=":
					delimiter = value[0:2]
					value = value[2:]
				elif value[0] == ">" or value[0] == "<" or value[0] == "~" or value[0] == "^":
					delimiter = value[0]
					value = value[1:]
				elif value[0] == "*" or value == "latest":
					delimiter = value
					try:
						value = ecosystemDataManager.getPackage(key).getLastestVersion().getName()
					except Exception as e:
						print(package.getName() + "@" + metadataVersion, "FETCHING", key, e)
						fetchNpm(ecosystemDataManager.getPackage(key))
						value = ecosystemDataManager.getPackage(key).getLastestVersion().getName()
				dependencyPackage = ecosystemDataManager.addPackage(key)
				dependencyVersion = dependencyPackage.addVersion(value)
				dependency = version.addDependency(dependencyVersion)
				dependency.setDelimiter(delimiter)
				dependency.setRequirements(requirements)
			except Exception as e:
				print(package.getName() + "@" + metadataVersion, "no dependencies", e)

def fetchRubygemsPackages():
	registry = 'https://rubygems.org/'
	packages = getContent(os.path.join(registry, 'versions'))
	packages = packages.split("\n")
	packages.pop(0)
	packages.pop(0)
	del packages[len(packages) - 1]
	for package in packages:
		split = package.split(" ")
		RUBYGEMS_PACKAGES_HAS_VERSIONS[split[0]] = split[1].split(",")
	return RUBYGEMS_PACKAGES_HAS_VERSIONS

def fetchRubygems(package):
	ecosystemDataManager = package.getEcosystemDataManager()
	registry = 'https://rubygems.org/api/v2/rubygems/'
	versions = RUBYGEMS_PACKAGES_HAS_VERSIONS[package.getName()]
	for metadataVersion in versions:
		try:
			metadata = getJson(os.path.join(registry, package.getName(), "versions", metadataVersion + ".json"))
			version = package.addVersion(metadataVersion)
			try:
				version.setLicenses(metadata["licenses"])
			except Exception as e:
				print(package.getName() + "@" + metadataVersion, "no licenses")
			try:
				version.addLicense(metadata["license"])
			except Exception as e:
				print(package.getName() + "@" + metadataVersion, "no license")
			version.setDatetime(metadata["created_at"])
			version.setAuthor(metadata["authors"])
			version.setEmail(metadata["mailing_list_uri"])
			version.setDownloads(metadata["version_downloads"])
			try:
				for metadataDependency in metadata["dependencies"]["runtime"]:
					key = metadataDependency["name"]
					value = metadataDependency["requirements"]
					requirements = value
					split = value.replace("x", "0").split(" ")
					delimiter = split[0]
					value = split[1]
					dependencyPackage = ecosystemDataManager.addPackage(key)
					dependencyVersion = dependencyPackage.addVersion(value)
					dependency = version.addDependency(dependencyVersion)
					dependency.setDelimiter(delimiter)
					dependency.setRequirements(requirements)
			except Exception as e:
				print(package.getName() + "@" + metadataVersion, "no dependencies")
		except Exception as e:
			print(package.getName() + "@" + metadataVersion, "VERSION FETCH FAIL")

def fetchCran(package):
	ecosystemDataManager = package.getEcosystemDataManager()
	registry = "https://cran.r-project.org/web/packages/"
	metadata = getContent(os.path.join(registry, package.getName()))
	soup = BeautifulSoup(metadata, "lxml")
	table = soup.find("table")
	dependencies = []
	for tr in table.findAll("tr"):
		td = tr.findAll("td")
		if (td[0].getText() == "Version:"):
			metadataVersion = td[1].getText().replace("\n", "")
		elif (td[0].getText() == "License:"):
			licenses = td[1].getText().replace("\n", "").split(", ")
		elif (td[0].getText() == "Depends:"):
			dependencies += td[1].getText().replace("\n", "").split(", ")
		elif (td[0].getText() == "Imports:"):
			dependencies += td[1].getText().replace("\n", "").split(", ")
		elif (td[0].getText() == "Published:"):
			datetime = td[1].getText().replace("\n", "")
		elif (td[0].getText() == "Maintainer:"):
			split = td[1].getText().replace("\n", "").replace(">", "").split("<")
			author = split[0].strip()
			email = split[1].strip()
	version = package.addVersion(metadataVersion)
	version.setLicenses(licenses)
	version.setDatetime(datetime)
	version.setAuthor(author)
	version.setEmail(email)
	for metadataDependency in dependencies:
		split = metadataDependency.replace("(", "").replace(")", "").split(" ")
		value = None
		delimiter = None
		key = split[0]
		if len(split) > 2:
			delimiter = split[1]
			value = split[2]
		elif len(split) == 2:
			value = split[1]
		requirements = metadataDependency
		dependencyPackage = ecosystemDataManager.addPackage(key)
		dependencyVersion = dependencyPackage.addVersion(value)
		dependency = version.addDependency(dependencyVersion)
		dependency.setDelimiter(delimiter)
		dependency.setRequirements(requirements)

def fetch(ecossystem, package):
	try:
		if ecossystem == "npm":
			fetchNpm(package)
		elif ecossystem == "rubygems":
			fetchRubygems(package)
		elif ecossystem == "cran":
			fetchCran(package)
	except Exception as e:
		print(package.getName(), "NO NETWORK CONNECTION. FETCH FAIL", e)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecossystem> [<limit> [<home>]]")
		sys.exit(1)
	if len(sys.argv) > 2:
		limit = int(sys.argv[2])
	else:
		limit = -1
	if len(sys.argv) > 3:
		home = sys.argv[3]
	else:
		home = ""
	ecossystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecossystem, home)
	packages = ecosystemDataManager.getPackages()
	if ecossystem == "rubygems":
		fetchRubygemsPackages()
	index = 0
	size = len(packages)
	for package in packages:
		print(index, "/", limit, "/", size)
		fetch(ecossystem, package)
		index += 1
		if index == limit:
			break
	ecosystemDataManager.save()
import sys
import os
import requests
import json
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

def getContent(url):
	request = requests.get(url)
	if request.status_code != 200:
		raise Exception
	return request.text.encode('utf-8')

def fetchNpm():
	registry = 'https://skimdb.npmjs.com/registry/'
	packages = getContent(os.path.join(registry, '_all_docs'))
	packages = json.loads(packages)
	packages = packages["rows"]
	packageNames = []
	for package in packages:
		packageNames.append(package["id"])
	return packageNames

def fetchRubygems():
	registry = 'https://rubygems.org/'
	packages = getContent(os.path.join(registry, 'versions'))
	packages = packages.split("\n")
	packages.pop(0)
	packages.pop(0)
	packageNames = []
	for package in packages:
		packageNames.append(package.split(" ")[0])
	return packageNames

def fetch(ecossystem):
	if ecossystem == "npm":
		return fetchNpm()
	elif ecossystem == "rubygems":
		return fetchRubygems()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecossystem>")
		sys.exit(1)
	ecossystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecossystem)
	packages = fetch(ecossystem)
	for package in packages:
		ecosystemDataManager.addPackage(package)
	ecosystemDataManager.save()
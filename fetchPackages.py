import sys
import os
import requests
import json
from bs4 import BeautifulSoup
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

def getContent(url):
	request = requests.get(url)
	if request.status_code != 200:
		raise Exception
	return request.text

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
	del packages[len(packages) - 1]
	packageNames = []
	for package in packages:
		packageNames.append(package.split(" ")[0])
	return packageNames

def fetchCran():
    registry = "https://cran.r-project.org/web/packages/available_packages_by_name.html"
    packages = getContent(registry)
    soup = BeautifulSoup(packages, "lxml")
    packageNames = []
    for link in soup.findAll('a'):
        if ('../../web/packages' in link.get('href')):
            packageNames.append(link.getText())
    return packageNames

def fetch(ecossystem):
	if ecossystem == "npm":
		return fetchNpm()
	elif ecossystem == "rubygems":
		return fetchRubygems()
	elif ecossystem == "cran":
		return fetchCran()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecossystem> [<limit>]")
		sys.exit(1)
	if len(sys.argv) == 3:
		limit = int(sys.argv[2])
	else:
		limit = -1
	ecossystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecossystem)
	packages = fetch(ecossystem)
	index = 0
	for package in packages:
		ecosystemDataManager.addPackage(package)
		index += 1
		if index == limit:
			break
	ecosystemDataManager.save()
import sys
import os
import requests
import json
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

def getContent(url):
    request = requests.get(url)
    if request.status_code != 200:
        raise Exception
    return request.text

def getJson(url):
    return json.loads(getContent(url))

def fetchNpm(package):
    ecosystemDataManager = package.getEcosystemDataManager()
    registry = 'https://registry.npmjs.org'
    metadata = getJson(os.path.join(registry, package.getName()))
    try:
        package.setTags(metadata["keywords"])
    except Exception as e:
        print(package.getName(), "no keyworks")
    try:
        package.setRepository(metadata["repository"]["url"])
    except Exception as e:
        print(package.getName(), "no repository")
    for metadataVersion in metadata["versions"]:
        version = package.addVersion(metadataVersion)
        try:
            for license in metadata["versions"][metadataVersion]["licenses"]:
                version.addLicense(license["type"])
        except Exception as e:
            print(package.getName() + "@" + metadataVersion, "no licenses")
        try:
            licenses.append(metadata["versions"][metadataVersion]["license"])
        except Exception as e:
            print(package.getName() + "@" + metadataVersion, "no license")
        version.setDatetime(metadata["time"][metadataVersion])
        try:
            for metadataDependency in metadata["versions"][metadataVersion]["dependencies"]:
                key = metadata["versions"][metadataVersion]["dependencies"][metadataDependency]
                value = metadataDependency
                requirements = value
                value = value.split(" ")[0]
                value = value.replace("x", "0")
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
                        fetchNpm(ecosystemDataManager.getPackage(key))
                        value = ecosystemDataManager.getPackage(key).getLastestVersion().getName()
                dependencyPackage = ecosystemDataManager.addPackage(key)
                dependencyVersion = dependencyPackage.addVersion(value)
                dependency = version.addDependency(dependencyVersion)
                dependency.setDelimiter(delimiter)
                dependency.setRequirements(requirements)
        except Exception as e:
            print(package.getName() + "@" + metadataVersion, "no dependencies")

RUBYGEMS_PACKAGES_HAS_VERSIONS = {}

def fetchRubygemsPackages():
    registry = 'https://rubygems.org/'
    packages = getContent(os.path.join(registry, 'versions'))
    packages = packages.split("\n")
    packages.pop(0)
    packages.pop(0)
    for package in packages:
        split = package.split(" ")
        RUBYGEMS_PACKAGES_HAS_VERSIONS[split[0]] = split[1].split(",")
    return RUBYGEMS_PACKAGES_HAS_VERSIONS

def fetchRubygems(package):
    ecosystemDataManager = package.getEcosystemDataManager()
    registry = 'https://rubygems.org/api/v2/rubygems/'
    versions = RUBYGEMS_PACKAGES_HAS_VERSIONS[package.getName()]
    for metadataVersion in versions:
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

def fetch(ecossystem, package):
    if ecossystem == "npm":
        fetchNpm(package)
    elif ecossystem == "rubygems":
        fetchRubygems(package)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "<ecossystem>")
        sys.exit(1)
    ecossystem = sys.argv[1]
    ecosystemDataManager = EcosystemDataManager(ecossystem)
    packages = ecosystemDataManager.getPackages()
    limit = 0
    if ecossystem == "rubygems":
        fetchRubygemsPackages()
    for package in packages:
        fetch(ecossystem, package)
        limit += 1
        if limit == 1000:
            break
    ecosystemDataManager.save()
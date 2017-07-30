from ecossystemDataManager import EcossystemDataManager

ecossystemDataManager = EcossystemDataManager("rubygems")
package = ecossystemDataManager.getPackage("json")
versions = package.getVersions()
version = versions[2]
context = version.getContext()
print(context)
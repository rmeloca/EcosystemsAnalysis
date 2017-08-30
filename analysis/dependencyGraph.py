
from ecossystemDataManager import EcossystemDataManager

if __name__ == '__main__':
    ecossystemDataManager = EcossystemDataManager("cran")
    packages_name = ecossystemDataManager.getPackagesHasIndex()
    for package in packages_name:
        versions = package.getVersions()    
        print(versions)
    #version = versions[0]
    #print(version)
    #context = version.getContext()
    #print(context)
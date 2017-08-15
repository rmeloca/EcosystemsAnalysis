from ecossystemDataManager import EcossystemDataManager

if __name__ == '__main__':
    ecossystemDataManager = EcossystemDataManager("cran")
    package = ecossystemDataManager.getPackage("rAltmetric")
    versions = package.getVersions()
    version = versions[0]
    context = version.getContext()
    print(context)
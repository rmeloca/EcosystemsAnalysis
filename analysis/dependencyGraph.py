
from ecossystemDataManager import EcossystemDataManager

#MOST_POPULARITY = ["R", "methods", "stats", "MASS", "graphics", "ggplot2", "utils", "Matrix", "survival", "mvtnorm", "lattice", "parallel", "Rcpp", "sp", "grDevices", "igraph", "ape", "grid", "tcltk", "splines", "coda", "nlme", "foreach", "rgl", "zoo", "raster", "boot", "plyr", "rJava", "data.table", "XML", "RCurl", "glmnet", "lme4", "stringr", "mgcv", "numDeriv", "gtools", "car", "Hmisc"]
#MOST_POPULARITY = ["commander@2.9.0", "mkdirp@0.5.1", "debug@2.2.0", "underscore@1.8.3", "lodash@2.4.1", "chalk@1.1.3", "lodash@3.10.1", "colors@1.1.2", "async@0.9.0", "minimist@1.2.0", "q@1.4.1", "lodash@4.17.4", "chalk@1.1.1", "chalk@1.0.0", "mkdirp@0.5.0", "express@4.14.0", "classnames@2.2.5", "lodash@4.13.1", "co@4.6.0", "async@1.5.2", "express@4.13.4", "express@4.13.3", "extend@3.0.0", "gulp@3.9.1", "fs-extra@0.30.0", "colors@0.6.2", "async@0.2.9", "optimist@0.6.1", "commander@2.8.1", "gulp-util@3.0.7", "underscore@1.7.0", "underscore@1.6.0", "node-uuid@1.4.7", "moment@2.10.6", "lodash@4.15.0", "open@0.0.5", "through2@2.0.0", "body-parser@1.15.2", "path@0.12.7", "gulp-rename@1.2.2"]
MOST_POPULARITY = ["json", "activesupport", "nokogiri", "thor", "rake", "httparty", "rest-client", "rack", "jquery-rails", "faraday"]
#, "sinatra@0", "i18n@0", "multi_json@0", "highline@0", "rails@0", "haml@0", "activesupport@3.0.0", "thor@0.19", "hashie@0", "colorize@0", "nokogiri@1.6", "activerecord@0", "redis@0", "json@1.8", "thor@0.19.1", "rails@3.0.0", "activesupport@3.0", "builder@0", "rspec@0", "trollop@0", "rest-client@1.6.7", "net-ssh@0", "faraday@0.9", "addressable@0", "activemodel@0", "rails@4.0", "rails@4.0.0", "rails@3.2", "sass-rails@0", "awesome_print@"]

VERSION_VISITED_OCURRENCES = []
VERSION_VISITED_DEPENDENCIES = []

VERTICES = []

def getTop10Packages(edm):
    versions = []
    i = 0
    for package_name in MOST_POPULARITY:
        versions.append(edm.getPackage(package_name).getVersion('0'))
        #i +=1
        #if (i == 10):
        #    break
    return versions
    

#ocurrence.getVersion().getGlobalRegularityRate()
#dependencie.getVersion.getGlobalRegularityRate()

def recursivaOcurrences(ocurrence):
    version = ocurrence.getOutVersion()
    #print (version.getPackage().getName())
    if (version in VERSION_VISITED_OCURRENCES):
        return
    VERSION_VISITED_OCURRENCES.append(version)
    ocurrences = version.getOcurrences()
    for o in ocurrences:
        recursivaOcurrences(o)

def recursivaDependencies(dependencie):
    version = dependencie.getInVersion()
    #print (version.getPackage().getName())
    if (version in VERSION_VISITED_DEPENDENCIES):
        return
    VERSION_VISITED_DEPENDENCIES.append(version)
    dependencies = version.getDependencies()
    for d in dependencies:
        recursivaDependencies(d)

def buildTree(versions):
    global VERTICES
    for version in versions:
        ocurrences = version.getOcurrences()
        edge = []
        edge.append(version)
        for o in ocurrences:
            edge.append(o.getOutVersion())
            VERTICES.append(edge)
            edge = []
            #print (o)
            recursivaOcurrences(o)
        #dependencies = version.getDependencies()
        #for d in dependencies:
        #    #print (d)
        #    recursivaDependencies(d)

if __name__ == '__main__':
    ecossystemDataManager = EcossystemDataManager("rubygems")
    versions = getTop10Packages(ecossystemDataManager)
    buildTree(versions)
    #print (VERTICES)
    for vertice in VERTICES:
        print (vertice[0].getPackage().getName() + ','+ vertice[1].getPackage().getName())
    #print (packages)
    #packages_name = ecossystemDataManager.getPackages()
    
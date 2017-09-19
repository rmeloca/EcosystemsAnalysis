import json
import sys
import os
import csv
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

#MOST_POPULARITY = ["R", "methods", "stats", "MASS", "graphics", "ggplot2", "utils", "Matrix", "survival", "mvtnorm", "lattice", "parallel", "Rcpp", "sp", "grDevices", "igraph", "ape", "grid", "tcltk", "splines", "coda", "nlme", "foreach", "rgl", "zoo", "raster", "boot", "plyr", "rJava", "data.table", "XML", "RCurl", "glmnet", "lme4", "stringr", "mgcv", "numDeriv", "gtools", "car", "Hmisc"]
#MOST_POPULARITY = ["commander@2.9.0", "mkdirp@0.5.1", "debug@2.2.0", "underscore@1.8.3", "lodash@2.4.1", "chalk@1.1.3", "lodash@3.10.1", "colors@1.1.2", "async@0.9.0", "minimist@1.2.0", "q@1.4.1", "lodash@4.17.4", "chalk@1.1.1", "chalk@1.0.0", "mkdirp@0.5.0", "express@4.14.0", "classnames@2.2.5", "lodash@4.13.1", "co@4.6.0", "async@1.5.2", "express@4.13.4", "express@4.13.3", "extend@3.0.0", "gulp@3.9.1", "fs-extra@0.30.0", "colors@0.6.2", "async@0.2.9", "optimist@0.6.1", "commander@2.8.1", "gulp-util@3.0.7", "underscore@1.7.0", "underscore@1.6.0", "node-uuid@1.4.7", "moment@2.10.6", "lodash@4.15.0", "open@0.0.5", "through2@2.0.0", "body-parser@1.15.2", "path@0.12.7", "gulp-rename@1.2.2"]
#MOST_POPULARITY = ["json", "activesupport", "nokogiri", "thor", "rake", "httparty", "rest-client", "rack", "jquery-rails", "faraday"]
#, "sinatra@0", "i18n@0", "multi_json@0", "highline@0", "rails@0", "haml@0", "activesupport@3.0.0", "thor@0.19", "hashie@0", "colorize@0", "nokogiri@1.6", "activerecord@0", "redis@0", "json@1.8", "thor@0.19.1", "rails@3.0.0", "activesupport@3.0", "builder@0", "rspec@0", "trollop@0", "rest-client@1.6.7", "net-ssh@0", "faraday@0.9", "addressable@0", "activemodel@0", "rails@4.0", "rails@4.0.0", "rails@3.2", "sass-rails@0", "awesome_print@"]
#t = ['json@0', 'activesupport@0', 'nokogiri@0', 'thor@0', 'rake@0', 'httparty@0', 'rest-client@0', 'rack@0', 'jquery-rails@0', 'faraday@0', 'sinatra@0', 'i18n@0', 'multi_json@0', 'highline@0', 'rails@0', 'haml@0', 'activesupport@3.0.0', 'thor@0.19', 'hashie@0', 'colorize@0', 'nokogiri@1.6', 'activerecord@0', 'redis@0', 'json@1.8', 'thor@0.19.1', 'rails@3.0.0', 'activesupport@3.0', 'builder@0']
VERSION_VISITED = []

EDGES = []
VERTICES = []


def buildTreePackageDependencies(version):
    for dependency in version.getDependencies():
        if (str(dependency.getInVersion().getName()) not in VERSION_VISITED):
            EDGES.append([version.getPackage().getName()+'@'+ version.getName(), dependency.getInVersion().getPackage().getName()+'@'+ dependency.getInVersion().getName()])
            VERTICES.append(dependency.getInVersion().getPackage().getName()+'@'+ dependency.getInVersion().getName())
            VERSION_VISITED.append(str(dependency.getInVersion().getName()))
        buildTreePackageDependencies(dependency.getInVersion())

def buildTreePackageOcurrences(version):
    for ocurrence in version.getOcurrences():
        if (str(ocurrence.getInVersion().getName()) not in VERSION_VISITED):
            EDGES.append([ocurrence.getInVersion().getPackage().getName()+'@'+ ocurrence.getInVersion().getName(), version.getPackage().getName()+'@'+ version.getName()])
            VERTICES.append(ocurrence.getInVersion().getPackage().getName()+'@'+ ocurrence.getInVersion().getName())
            VERSION_VISITED.append(str(ocurrence.getInVersion().getName()))
        buildTreePackageOcurrences(ocurrence.getInVersion())
    
def generateXmlGraph():
    treePackage = []

    edges = []
    edges.append(["a","b"])
    edges.append(["a","c"])
    edges.append(["b","c"])


    treePackage.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    treePackage.append("<gexf xmlns=\"http://www.gexf.net/1.2draft\" xmlns:viz=\"http://www.gexf.net/1.1draft/viz\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd\" version=\"1.2\"> \n")
    treePackage.append("<graph> \n <nodes>")
    for vertex in VERTICES:
        treePackage.append("<node id=\""+vertex+"\" label=\""+vertex+"\"> <viz:color r=\"113\" g=\"203\" b=\"157\" a=\"0.6\"/> <viz:size value=\"3\"/> <viz:shape value=\"disc\"/></node>")

    treePackage.append("</nodes> \n <edges>")
    i = 0
    for edge in EDGES:
        treePackage.append("<edge id=\""+str(i)+"\" source=\""+edge[0]+"\" target=\""+edge[1]+"\"><viz:color r=\"0\" g=\"0\" b=\"0\" a=\"0.6\"/></edge>")
        i += 1
    treePackage.append("</edges> \n </graph> \n </gexf>")

    f = open('teste2.gexf', 'w')
    for line in treePackage:
        f.write(str(line+"\n"))

    f.close()

if __name__ == '__main__':
    ecosystemDataManager = EcosystemDataManager("rubygems")

    package = ecosystemDataManager.getPackage('faraday')
    print(package.getName())
    #most_popular_version = package.getMostPopularVersions(1)[0]
    most_popular_version = package.getVersion("1")
    print(most_popular_version.getName())
    VERTICES.append(package.getName()+'@'+ most_popular_version.getName())
    buildTreePackageOcurrences(most_popular_version)
    buildTreePackageDependencies(most_popular_version)
  

    generateXmlGraph()

import json
import sys
import os
import csv
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

VERSION_VISITED_OCURRENCES = []
VERSION_VISITED_DEPENDENCIES = []

VERTICES = []

def recursivaOcurrences(ocurrence):
    global VERTICES
    global VERSION_VISITED_OCURRENCES
    version = ocurrence.getOutVersion()
    if (version in VERSION_VISITED_OCURRENCES):
        return
    VERSION_VISITED_OCURRENCES.append(version)
    ocurrences = version.getOcurrences()
    for o in ocurrences:
        VERTICES.append([version, o.getOutVersion()])
        recursivaOcurrences(o)

def recursivaDependencies(dependencie):
    global VERTICES
    global VERSION_VISITED_DEPENDENCIES
    version = dependencie.getInVersion()
    if (version in VERSION_VISITED_DEPENDENCIES):
        return
    VERSION_VISITED_DEPENDENCIES.append(version)
    dependencies = version.getDependencies()
    for d in dependencies:
        VERTICES.append([version, o.getInVersion()])
        recursivaDependencies(d)

def buildTree(versions):
    global VERTICES
    for version in versions:
        ocurrences = version.getOcurrences()
        #print (ocurrences)
        for o in ocurrences:
            VERTICES.append([version, o.getInVersion()])
            recursivaOcurrences(o)
        #dependencies = version.getDependencies()
        #for d in dependencies:
        #    recursivaDependencies(d)

def recursivaOcurrences2(ocurrence):
    global VERTICES
    global VERSION_VISITED_OCURRENCES
    version = ocurrence.getOutVersion()
    ocurrences = version.getOcurrences()
    for o in ocurrences:
        if (o.getInVersion().getPackage().getName() not in VERSION_VISITED_OCURRENCES):
            VERSION_VISITED_OCURRENCES.append(o.getInVersion().getPackage().getName())
            VERTICES.append([version.getPackage().getName(), o.getInVersion().getPackage().getName()])
            recursivaOcurrences2(o)

def buildTreePackage(version):
    for o in version.getOcurrences():
        if (o.getInVersion() not in VERSION_VISITED_OCURRENCES):
            VERTICES.append([version.getPackage().getName()+'@'+ version.getName(), o.getInVersion().getPackage().getName()+'@'+ o.getInVersion().getName()])
        VERSION_VISITED_OCURRENCES.append(o.getInVersion())
        buildTreePackage(o.getInVersion())
    for dependency in version.getDependencies():
        if (dependency.getInVersion() not in VERSION_VISITED_OCURRENCES):
            VERTICES.append([version.getPackage().getName()+'@'+ version.getName(), dependency.getInVersion().getPackage().getName()+'@'+ dependency.getInVersion().getName()])
        VERSION_VISITED_OCURRENCES.append(dependency.getInVersion())
        buildTreePackage(dependency.getInVersion())

if __name__ == '__main__':
    ecosystemDataManager = EcosystemDataManager("rubygems")
    #packages = ecosystemDataManager.getMostPopularPackages(1)
    version = ecosystemDataManager.getMostPopularVersions()[0]

    package = ecosystemDataManager.getPackage('Capcode')
    print(package.getName())
    print(package.getMostPopularVersions(1)[0].getName())
    #print (version.getOcurrences())
    buildTreePackage(package.getMostPopularVersions(1)[0])
    #print (VERSION_VISITED_OCURRENCES)
    #print (VERTICES)
    #buildTree(version)

    with open('Capcode.csv', 'w') as csvfile:
        fieldnames = ['v1', 'v2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for vertice in VERTICES:
            #print (vertice[0] + ", " + vertice[1])
            writer.writerow({'v1': vertice[0], 'v2': vertice[1]})
    
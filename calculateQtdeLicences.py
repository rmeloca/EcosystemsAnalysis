from edm import *
import json

unlisted = "unlisted.json"
osi = "osi.json"

allUnlistedLicense = 0
allOSI = 0

with open(unlisted) as file:
	unlisted = json.load(file)
with open(osi) as file:
	osi = json.load(file)

edm = EcosystemDataManager("cran")
licenses = edm.get("VersionsHasLicenses")
cranlicenses = [y for x in licenses for y in x]
print ("Cran Total Licenses" , len(cranlicenses))
crandistinctlicenses = list(set(cranlicenses))
unlistedLicense = 0
osiLicense = 0
misused = 0
for license in crandistinctlicenses:
    if (license in osi):
        osiLicense += 1
    elif (license in unlisted):
        unlistedLicense += 1
    elif (license != "file" and license != "copyright" and license != "none"):
        misused += 1
print ("Cran Distinct Licenses: "+ str(len(crandistinctlicenses)))
print ("Cran OSI Licenses known: " + str(osiLicense))
print ("Cran Unlisted Licenses unapproved: " + str(unlistedLicense))
print("Cran copyright", "copyright" in crandistinctlicenses)
print("Cran none", "none" in crandistinctlicenses)
print("Cran file", "file" in crandistinctlicenses)
print("Cran misused", misused)
print()

edm = EcosystemDataManager("rubygems")
licenses = edm.get("VersionsHasLicenses")
rubylicenses = [y for x in licenses for y in x]
print ("RubyGems Total Licenses" , len(rubylicenses))
rubydistinctlicenses = list(set(rubylicenses))
unlistedLicense = 0
osiLicense = 0
misused = 0
for license in rubydistinctlicenses:
    if (license in osi):
        osiLicense += 1
    elif (license in unlisted):
        unlistedLicense += 1
    elif (license != "file" and license != "copyright" and license != "none"):
        misused += 1
print ("RubyGems Distinct Licenses: "+ str(len(rubydistinctlicenses)))
print ("RubyGems OSI Licenses: " + str(osiLicense))
print ("RubyGems Unlisted Licenses: " + str(unlistedLicense))
print("Rubygems copyright", "copyright" in rubydistinctlicenses)
print("Rubygems none", "none" in rubydistinctlicenses)
print("Rubygems file", "file" in rubydistinctlicenses)
print("Rubygems misused", misused)
print()

edm = EcosystemDataManager("npm")
licenses = edm.get("VersionsHasLicenses")
npmlicenses = [y for x in licenses for y in x]
print ("NPM Total Licenses" , len(npmlicenses))
npmdistinctlicenses = list(set(npmlicenses))
unlistedLicense = 0
osiLicense = 0
misused = 0
for license in npmdistinctlicenses:
    if (license in osi):
        osiLicense += 1
    elif (license in unlisted):
        unlistedLicense += 1
    elif (license != "file" and license != "copyright" and license != "none"):
        misused += 1
print ("NPM Distinct Licenses: "+ str(len(npmdistinctlicenses)))
print ("NPM OSI Licenses: " + str(osiLicense))
print ("NPM Unlisted Licenses: " + str(unlistedLicense))
print("NPM copyright", "copyright" in npmdistinctlicenses)
print("NPM none", "none" in npmdistinctlicenses)
print("NPM file", "file" in npmdistinctlicenses)
print("NPM misused", misused)
print()

allecosystems = crandistinctlicenses + rubydistinctlicenses + npmdistinctlicenses
alldistinct = list(set(allecosystems))
inosi = [x for x in alldistinct if x in osi]


inUnlitesd = [x for x in alldistinct if x in unlisted]

print ("All Unlisted Licenses: " + str(len(unlisted)))
print ("All OSI Licenses: " + str(len(inosi)))
print ("All Distinct Licenses: " + str(len(alldistinct)))
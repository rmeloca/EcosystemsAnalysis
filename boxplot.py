import json
import sys
import os
import csv
import plotly
import plotly.graph_objs as go
import numpy as np
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

#def getLocalRegularityRate(self):
#    localRegularityRate = []
#    for version in self.getVersions():
#        localRegularityRate.append(version.getLocalRegularityRate())
#    return localRegularityRate


def plotBoxPlot(vector):
    trace0 = go.Box(
        y=vector
    )
    data = [trace0]
    plotly.offline.plot(data)


if __name__ == '__main__':
    ecosystemDataManager = EcosystemDataManager("rubygems")
    packageSizeDistribution = ecosystemDataManager.getPackageSizeDistribution()
    print (packageSizeDistribution)
    plotBoxPlot(packageSizeDistribution)
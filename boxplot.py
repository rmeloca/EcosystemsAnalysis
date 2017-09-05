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


def histogram(vector, name_histogram):
    trace = go.Histogram(
        name='Results',
        x = vector,
        xbins=dict(
            start=1,
            end=150,
            size=0.5
        )
    )
    data = [trace]
    plotly.offline.plot(data, filename=name_histogram)
    

def plotBoxPlot(vector, name_boxplot):
    trace0 = go.Box(
        y=vector
    )
    data = [trace0]
    plotly.offline.plot(data, filename=name_boxplot)


if __name__ == '__main__':
    ecosystemDataManager = EcosystemDataManager("npm")
    packageSizeDistribution = ecosystemDataManager.getPackageSizeDistribution()
    print (packageSizeDistribution)
    plotBoxPlot(packageSizeDistribution, 'boxplot_packageSizeDistribution')
    histogram(packageSizeDistribution, 'histogram_packageSizeDistribution')
import sys
import os
import plotly
import plotly.offline as offline
import plotly.graph_objs as go
import math
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

def plotHistogram(vector, name_histogram):
	trace = go.Histogram(
		name='Results',
		x = vector,
		xbins=dict(
			start=1,
			end=50,
			size=0.5
		)
	)
	data = [trace]
	plotly.offline.plot(data, filename=name_histogram)

def plotHistograms(vectors, name_histogram):
	data = []
	for vector in vectors:
		trace = go.Histogram(
			x = vectors[vector],
			name = vector,
			xbins=dict(
				start=0,
				end=2,
				size=0.1,
			)
		)
		data.append(trace)
	plotly.offline.plot(data, filename=name_histogram)
	

def plotBoxPlot(vector, name_boxplot):
	trace0 = go.Box(
		y=vector,
	)
	data = [trace0]
	plotly.offline.plot(data, filename=name_boxplot)

def plotMultBoxPlot(vectors, name_boxplot):
	data = []
	for vector in vectors:
		trace = go.Box(
			y=vectors[vector],
			boxpoints='all',
			name=vector
		)
		data.append(trace)
	plotly.offline.plot(data, filename=name_boxplot)

def plorBarChart(vector_x, vector_y, nameBarChart):
	data = [go.Bar(
	        x=vector_x,
	        y=vector_y
	)]	
	plotly.offline.plot(data, filename=nameBarChart)


def plotMultBarsChart(setName, vector_x, vectors_y, nameBarChart):
	data = []
	i = 0
	for vector in vectors_y:
		trace = go.Bar(
			x=vector_x,
			y=vector,
			name=setName[i]
		)
		i += 1
		data.append(trace)
	layout = go.Layout(
		barmode='group'
	)
	fig = go.Figure(data=data, layout=layout)
	plotly.offline.plot(fig, filename=nameBarChart)

def plorScatterChart(vector_x, vector_y, nameBarChart):
	data = [go.Scatter(
	        x=vector_x,
	        y=vector_y,
			mode = 'lines+markers'
	)]	
	plotly.offline.plot(data, filename=nameBarChart)

def plotMultScatterChart(setName, vector_x, vectors_y, nameBarChart):
	data = []
	i = 0
	for vector in vectors_y:
		trace = go.Scatter(
			x=vector_x,
			y=vector,
			name=setName[i],
			mode = 'lines+markers'
		)
		i += 1
		data.append(trace)
	plotly.offline.plot(data, filename=nameBarChart)

def plotMostPopularLicenses(keys, values, chartName):
	trace = go.Bar(
		name=chartName,
		y = values,
		x = keys
	)
	data = [trace]
	plotly.offline.plot(data, filename=chartName)

def plotBubbleChart(values, chartName):
	trace0 = go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 11, 12, 13],
    mode='markers',
    marker=dict(
        size=[40, 60, 80, 100],
    	)
	)

	data = [trace0]
	plotly.offline.plot(data, filename=chartName)

def plotPackageHistory(package, chartName):
	historyVersions = package.getHistory()
	listLocalRegularityRate = []
	listGlobalRegularityRate = []
	listGlobalRegularityMean = []
	versionsName = []
	for version in historyVersions:
		versionsName.append(version.getName())
		listLocalRegularityRate.append((version.getLocalRegularityRate()))
		listGlobalRegularityRate.append((version.getGlobalRegularityRate()))
		listGlobalRegularityMean.append((version.getGlobalRegularityMean()))
	setName = ["Local Regularity Rate", "Global Regularity Rate", "Global Regularity Mean"]
	plotMultScatterChart(setName, versionsName, [listLocalRegularityRate, listGlobalRegularityRate, listGlobalRegularityMean], chartName)

def plotNumberDependenciesBetweenPackages(ecosystemDataManager):
	packages = ecosystemDataManager.getPackages()
	numeberDependecies = {}
	lenVersionsDependencies = []
	for package in packages:
		for version in package.getVersions():		
			lenVersionDependencies =  len(version.getDependencies())
			lenVersionsDependencies.append(lenVersionDependencies)
		numeberDependecies[package.getName()] = lenVersionsDependencies
	return lenVersionsDependencies

def popularVersionHistory(package, chartName):
	versionsOcurrences = []
	downloads = []
	nameVersions = []
	for version in package.getVersions():
		if (version.getDownloads() != None):
			versionsOcurrences.append((len(version.getOcurrences()) + int(version.getDownloads())))
			downloads.append(int(version.getDownloads()))
			nameVersions.append("version = " + version.getName())
	x = [i*2 for i in range(len(versionsOcurrences))]
	print(versionsOcurrences)
	print(downloads)
	print(x)
	trace0 = go.Scatter(
    	x=x,
    	y=downloads,
		name=package.getName(),
		text=nameVersions,
    	mode='markers',
    	marker=dict(
    	    size=versionsOcurrences,
			sizemode='area'
    		)
	)

	data = [trace0]
	plotly.offline.plot(data, filename=chartName)	

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [history[=<package>]] [package-size] [most-popular-metrics[=<most-popular-size>]] [licenses] [metrics]")
		sys.exit(1)
	if len(sys.argv) == 2:
		print("No options provided. all plots will be rendered")
		x = input('Can plots all charts? (Y/n): ')
		if (x == 'y' or x == 'Y'):
			options = {"history": None, "package-size": None, "most-popular-metrics": None, "licenses": None, "metrics": None}
		else:
			print ("No charts to render.")
			exit()
	else:
		options = {}
		for argument in sys.argv[2:]:
			split = argument.split("=")
			if len(split) > 1:
				options[split[0]] = split[1]
			else:
				options[split[0]] = None
	try:
		os.makedirs("visualizations")
	except Exception as e:
		pass
	ecosystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	iregularPackages = None
	if "package-size" in options:
		packageSizeDistribution = [len(package) for package in ecosystemDataManager.getPackages()]
		plotBoxPlot(packageSizeDistribution, "visualizations/" + ecosystem + '_boxplot_packageSizeDistribution.html')
		plotHistogram(packageSizeDistribution, "visualizations/" + ecosystem + '_histogram_packageSizeDistribution.html')
	if "most-popular-metrics" in options:
		mostPopularSize = options["most-popular-metrics"]
		if not mostPopularSize:
			print("<most-popular-size> not provided. Default size will be used")
			mostPopularSize = 10
		iregularPackages = ecosystemDataManager.getMostPopularIregularPackages(mostPopularSize)
		iregularPackagesHasLocalRegularityRates = {iregularPackage.getName(): iregularPackage.getLocalRegularityRates() for iregularPackage in iregularPackages}
		plotMultBoxPlot(iregularPackagesHasLocalRegularityRates, "visualizations/" + ecosystem + '_boxplot_regularityRateVersions.html')
		plotHistograms(iregularPackagesHasLocalRegularityRates, "visualizations/" + ecosystem + '_histogram_regularityRateVersions.html')
	if "licenses" in options:
		licenses = ecosystemDataManager.getMostPopularLicenses()
		plotMostPopularLicenses([str(k) for k, v in licenses], [v for k, v in licenses], "visualizations/" + ecosystem + "_bars_mostPopularLicenses.html")
		plotMostPopularLicenses([str(k) for k, v in licenses], [math.log10(v) for k, v in licenses], "visualizations/" + ecosystem + "_bars_log10_mostPopularLicenses.html")
	if "metrics" in options:
		metrics = {}
		metrics["Local Regularity Rate"] = ecosystemDataManager.getLocalRegularityRates()
		metrics["Global Regularity Rate"] = ecosystemDataManager.getGlobalRegularityRates()
		metrics["Global Regularity Mean"] = ecosystemDataManager.getGlobalRegularityMeans()
		plotMultBoxPlot(metrics, "visualizations/" + ecosystem + '_boxplot_metrics.html')
	if "history" in options:
		package = options["history"]
		if package:
			package = ecosystemDataManager.getPackage(package)
		else:
			print("<package> not provided. Most popular and iregular package will be used to plot their history")
			if not iregularPackages:
				iregularPackages = ecosystemDataManager.getMostPopularIregularPackages(1)
			package = iregularPackages[0]
		plotPackageHistory(package, "visualizations/" + ecosystem + "_" + package.getName() + '_regularity_rate_bars.html')
		popularVersionHistory(package, "visualizations/" + ecosystem + "_" + package.getName() + '_poupular_version.html')
	if "number-dependencies" in options:
		plotBoxPlot(plotNumberDependenciesBetweenPackages(ecosystemDataManager), "visualizations/" + ecosystem+"_number_dependencies_between_packages.html")
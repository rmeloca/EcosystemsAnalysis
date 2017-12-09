import sys
import os
import plotly
import plotly.offline as offline
import plotly.graph_objs as go
import math
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

"""
Functions to plot charts, all the plot is a html file;
"""

"""
Function to plot a histogram, most be put params: vector (numbers of histogram) and name to histogram.
"""
def plotHistogram(vector, name_histogram):
	trace = go.Histogram(
		name='Results',
		x = vector,
		xbins=dict(
			start=1,
			# end=50,
			size=0.5
		)
	)
	data = [trace]
	plotly.offline.plot(data, filename=name_histogram)

"""
Function to plot a range of hitograms, the params is a vector by vector.
"""
def plotHistograms(vectors, name_histogram):
	data = []
	for vector in vectors:
		trace = go.Histogram(
			x = vectors[vector],
			name = vector,
			xbins=dict(
				start=0,
				# end=2,
				size=0.1,
			)
		)
		data.append(trace)
	plotly.offline.plot(data, filename=name_histogram)

"""
Function to plot a boxplot, the params is a vector and name to boxplot.
"""
def plotBoxPlot(vector, name_boxplot):
	trace0 = go.Box(
		y=vector,
	)
	data = [trace0]
	plotly.offline.plot(data, filename=name_boxplot)

"""
Function to plot a range of boxplot, the params is a vector by vector and name to boxplot.
"""
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

"""
Function to plot a bar chart, the params is a vector with X positions, vector with Y positions
and name to barchart.
"""
def plorBarChart(vector_x, vector_y, nameBarChart):
	data = [go.Bar(
	        x=vector_x,
	        y=vector_y
	)]	
	plotly.offline.plot(data, filename=nameBarChart)

"""
Function to plot a range of bar chart, the params is a vector with name each barchart,
vector with X positions, vector with Y positions and name to barchart.
"""
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

"""
Function to plot a scatter plot chart, the params is vector with X positions,
vector with Y positions and name to scatter plot chart.
"""
def plorScatterChart(vector_x, vector_y, nameBarChart):
	data = [go.Scatter(
	        x=vector_x,
	        y=vector_y,
			mode = 'lines+markers'
	)]	
	plotly.offline.plot(data, filename=nameBarChart)

"""
Function to plot a scatter plot chart, the params is vector with X positions,
vector with Y positions and name to scatter plot chart.
"""
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

"""
Function to plot the most popular licenses in bar chart
"""
def plotMostPopularLicenses(keys, values, chartName):
	trace = go.Bar(
		name=chartName,
		y = values,
		x = keys
	)
	data = [trace]
	plotly.offline.plot(data, filename=chartName)

"""
Function to plot the package history using a mult scatter plot
"""
def plotPackageHistory(package, chartName):
	historyVersions = package.getHistory()
	listLocalRegularityRate = []
	listGlobalRegularityRate = []
	listGlobalRegularityMean = []
	versionsName = []
	for version in historyVersions:
		if version.getDatetime():
			versionsName.append(version.getName())
			listLocalRegularityRate.append((version.getLocalRegularityRate()))
			listGlobalRegularityRate.append((version.getGlobalRegularityRate()))
			listGlobalRegularityMean.append((version.getGlobalRegularityMean()))
	setName = ["Local Regularity Rate", "Global Regularity Rate", "Global Regularity Mean"]
	plotMultScatterChart(setName, versionsName, [listLocalRegularityRate, listGlobalRegularityRate, listGlobalRegularityMean], chartName)

def plotNumberDependenciesBetweenPackages(ecosystemDataManager):
	packages = ecosystemDataManager.getPackages()
	lenVersionsDependencies = []
	for package in packages:
		for version in package.getVersions():		
			lenVersionDependencies = len(version.getDependencies())
			lenVersionsDependencies.append(lenVersionDependencies)
	return lenVersionsDependencies

"""
Function to plot package history by versions, the out plot is a scatter plot.
"""
def popularVersionHistory(package, chartName):
	versionsOccurrences = []
	localRegularityRate = []
	globalRegularityRate = []
	globalRegularityMean = []
	nameVersions = []
	for version in package.getHistory():
		if version.getDatetime():
			versionsOccurrences.append(len(version.getOccurrences()))
			nameVersions.append("version = " + version.getName())
			localRegularityRate.append(version.getLocalRegularityRate())
			globalRegularityRate.append(version.getGlobalRegularityRate())
			globalRegularityMean.append(version.getGlobalRegularityMean())
	x = [i for i in range(len(versionsOccurrences))]
	trace0 = go.Scatter(
    	x=x,
    	y=localRegularityRate,
		name="Local Regularity Rate",
		text=nameVersions,
    	mode='markers',
    	marker=dict(
    	    size = versionsOccurrences,
			sizemode ='area',
    		)
	)
	trace1 = go.Scatter(
    	x=x,
    	y=globalRegularityRate,
		name="Global Regularity Rate",
		text=nameVersions,
    	mode='markers',
    	marker=dict(
    	    size = versionsOccurrences,
			sizemode ='area'
    		)
	)
	trace2 = go.Scatter(
    	x=x,
    	y=globalRegularityMean,
		name="Global Regularity Mean",
		text=nameVersions,
    	mode='markers',
    	marker=dict(
    	    size = versionsOccurrences,
			sizemode ='area'
    		)
	)
	data = [trace0, trace1, trace2]
	plotly.offline.plot(data, filename=chartName)	

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [history[=<package>]] [package-size] [most-popular-metrics[=<most-popular-size>]] [number-dependencies] ][licenses] [metrics]")
		sys.exit(1)
	if len(sys.argv) == 2:
		print("No options provided. all plots will be rendered")
		x = input('Can plots all charts? (Y/n): ')
		if (x == 'y' or x == 'Y'):
			options = {"history": None, "package-size": None, "most-popular-metrics": None, "licenses": None, "metrics": None, "number-dependencies": None}
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
	irregularPackages = None
	if "package-size" in options:
		packageSizeDistribution = [len(package) for package in ecosystemDataManager.getPackages()]
		plotBoxPlot(packageSizeDistribution, "visualizations/" + ecosystem + '_boxplot_packageSizeDistribution.html')
		plotHistogram(packageSizeDistribution, "visualizations/" + ecosystem + '_histogram_packageSizeDistribution.html')
	if "most-popular-metrics" in options:
		mostPopularSize = options["most-popular-metrics"]
		if not mostPopularSize:
			print("<most-popular-size> not provided. Default size will be used")
			mostPopularSize = 10
		irregularPackages = ecosystemDataManager.getMostPopularIrregularPackages(mostPopularSize)
		irregularPackagesHasLocalRegularityRates = {irregularPackage.getName(): irregularPackage.getLocalRegularityRates() for irregularPackage in irregularPackages}
		try: 
			plotMultBoxPlot(irregularPackagesHasLocalRegularityRates, "visualizations/" + ecosystem + '_boxplot_regularityRateVersions.html')
			plotHistograms(irregularPackagesHasLocalRegularityRates, "visualizations/" + ecosystem + '_histogram_regularityRateVersions.html')
		except Exception as e:
			pass
	if "licenses" in options:
		licensePerVersion = [len(licenses) for licenses in ecosystemDataManager.getLicensesPerVersion()]
		plotBoxPlot(licensePerVersion, "visualizations/" + ecosystem + '_boxplot_licensesPerVersion.html')
		licenses = ecosystemDataManager.getMostPopularLicenses(25)
		licenses = licenses[4]
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
			print("<package> not provided. Most popular and irregular package will be used to plot their history")
			if not irregularPackages:
				irregularPackages = ecosystemDataManager.getMostPopularIrregularPackages(1)
			try:
				package = irregularPackages[0]
				plotPackageHistory(package, "visualizations/" + ecosystem + "_" + package.getName() + '_regularity_rate_bars.html')
				popularVersionHistory(package, "visualizations/" + ecosystem + "_" + package.getName() + '_popular_version.html')
			except Exception as e:
				pass
	if "number-dependencies" in options:
		versionsHasDependencies = [len(version.getDependencies()) for package in ecosystemDataManager.getPackages() for version in package.getVersions()]
		plotBoxPlot(versionsHasDependencies, "visualizations/" + ecosystem+"_dependencies_between_packages")
	if "groups" in options:
		plotMultBarsChart([1,2], [2,3], [3], "teste.html")
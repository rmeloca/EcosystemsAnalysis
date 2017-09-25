import sys
import os
import plotly
import plotly.graph_objs as go
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
	trace = go.Histogram(
		name=chartName,
		x = keys,
		y = values	
	)
	data = [trace]
	plotly.offline.plot(data, filename=chartName)

def plotPackageHistory(package):
	historyVersions = package.getHistory()
	listLocalRegularityRate = []
	listGlobalRegularityRate = []
	versionsName = []
	for version in historyVersions:
		versionsName.append(version.getName())
		listLocalRegularityRate.append((version.calculateLocalRegularityRate()))
		listGlobalRegularityRate.append((version.calculateGlobalRegularityRate()))
	setName = ["Local Regularity Rate", "Global Regularity Rate"]
	plotMultScatterChart(setName, versionsName, [listLocalRegularityRate, listGlobalRegularityRate], package.getName() + '_regularity_rate_bars')

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [<package>]")
		sys.exit(1)
	ecosystem = sys.argv[1]
	if len(sys.argv) > 2:
		package = sys.argv[2]
	else:
		print("<package> not provided. Most popular and irregular package will be used to plot their history")
		package = None
	try:
		os.makedirs("visualizations")
	except Exception as e:
		pass
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	packageSizeDistribution = [len(package) for package in ecosystemDataManager.getPackages()]
	plotBoxPlot(packageSizeDistribution, "visualizations/" + ecosystem + '_boxplot_packageSizeDistribution.html')
	plotHistogram(packageSizeDistribution, "visualizations/" + ecosystem + '_histogram_packageSizeDistribution.html')
	irregularPackages = ecosystemDataManager.getMostPopularIrregularPackages(10)
	irregularPackagesHasLocalRegularityRates = {irregularPackage.getName(): irregularPackage.getLocalRegularityRates() for irregularPackage in irregularPackages}
	plotMultBoxPlot(irregularPackagesHasLocalRegularityRates, "visualizations/" + ecosystem + '_boxplot_regularityRateVersions.html')
	plotHistograms(irregularPackagesHasLocalRegularityRates, "visualizations/" + ecosystem + '_histogram_regularityRateVersions.html')
	licenses = ecosystemDataManager.getMostPopularLicenses()
	plotMostPopularLicenses([str(k) for k, v in licenses], [v for k, v in licenses], "visualizations/" + ecosystem + "_bars_mostPopularLicenses.html")
	if package:
		package = ecosystemDataManager.getPackage(package)
	else:
		package = irregularPackages[0]
	plotPackageHistory(package)
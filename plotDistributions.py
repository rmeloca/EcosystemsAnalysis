import sys
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

def mostPopularLicenses(ecosystemDataManager, ecosystemName, size = None):
	keys = []
	values = []
	for k, v in ecosystemDataManager.getMostPopularLicenses().items():
		keys.append(k)
		values.append(v)
	if size:
		keys = keys[:size]
		values = values[:size]
	trace = go.Histogram(
		name=ecosystemName,
		x = keys,
		y = values	
	)
	data = [trace]
	plotly.offline.plot(data, filename=ecosystemName)

def packageHistory(ecosystemDataManager, packageName):
	package = ecosystemDataManager.getPackage(packageName)
	historyVersions = package.getHistory()
	listLocalRegularityRate = []
	listGlobalRegularityRate = []
	versionsName = []
	for version in historyVersions:
		versionsName.append(version.getName())
		listLocalRegularityRate.append((version.calculateLocalRegularityRate()))
		listGlobalRegularityRate.append((version.calculateGlobalRegularityRate()))
	setName = ["Local Regularity Rate", "Global Regularity Rate"]
	plotMultScatterChart(setName ,versionsName, [listLocalRegularityRate, listGlobalRegularityRate], packageName+'_regularity_rate_bars')

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("Usage:", sys.argv[0], "<ecosystem> <package>")
		print("<package> to use in function 'packageHistory'")
		sys.exit(1)
	ecosystem = sys.argv[1]
	packageName = sys.argv[2]
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	packageSizeDistribution = [len(package) for package in ecosystemDataManager.getPackages()]
	plotBoxPlot(packageSizeDistribution, ecosystem + '_boxplot_packageSizeDistribution.html')
	plotHistogram(packageSizeDistribution, ecosystem + '_histogram_packageSizeDistribution.html')
	irregularPackages = ecosystemDataManager.getMostPopularIrregularPackages(10)
	irregularPackagesHasLocalRegularityRates = {irregularPackage.getName(): irregularPackage.getLocalRegularityRates() for irregularPackage in irregularPackages}
	plotMultBoxPlot(irregularPackagesHasLocalRegularityRates, ecosystem + '_boxplot_regularityRateVersions.html')
	plotHistograms(irregularPackagesHasLocalRegularityRates, ecosystem + '_histogram_regularityRateVersions.html')
	mostPopularLicenses(ecosystemDataManager, ecosystem, 10)
	packageHistory(ecosystemDataManager, packageName)
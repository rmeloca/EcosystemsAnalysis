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

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecossystem>")
		sys.exit(1)
	ecossystem = sys.argv[1]
	ecosystemDataManager = EcosystemDataManager(ecossystem)
	packageSizeDistribution = [len(package) for package in ecosystemDataManager.getPackages()]
	plotBoxPlot(packageSizeDistribution, ecossystem + '_boxplot_packageSizeDistribution.html')
	plotHistogram(packageSizeDistribution, ecossystem + '_histogram_packageSizeDistribution.html')
	irregularPackages = ecosystemDataManager.getMostPopularIrregularPackages(10)
	irregularPackagesHasLocalRegularityRates = {irregularPackage.getName(): irregularPackage.getLocalRegularityRates() for irregularPackage in irregularPackages}
	plotMultBoxPlot(irregularPackagesHasLocalRegularityRates, ecossystem + '_boxplot_regularityRateVersions.html')
	plotHistograms(irregularPackagesHasLocalRegularityRates, ecossystem + '_histogram_regularityRateVersions.html')
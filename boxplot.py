import sys
import plotly
import plotly.graph_objs as go
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

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
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "<ecossystem>")
        sys.exit(1)
    ecossystem = sys.argv[1]
    ecosystemDataManager = EcosystemDataManager(ecossystem)
    packageSizeDistribution = ecosystemDataManager.getPackageSizeDistribution()
    plotBoxPlot(packageSizeDistribution, 'boxplot_packageSizeDistribution')
    histogram(packageSizeDistribution, 'histogram_packageSizeDistribution')
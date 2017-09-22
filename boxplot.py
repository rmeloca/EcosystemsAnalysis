import sys
import plotly
import plotly.graph_objs as go
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

def plotBoxPlot(vector):
    trace0 = go.Box(
        y=vector
    )
    data = [trace0]
    plotly.offline.plot(data)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "<ecossystem>")
        sys.exit(1)
    ecossystem = sys.argv[1]
    ecosystemDataManager = EcosystemDataManager(ecossystem)
    packageSizeDistribution = ecosystemDataManager.getPackageSizeDistribution()
    plotBoxPlot(packageSizeDistribution)
import string

class MultiDataPlotter:
    #TODO:
    #"filter" functions for dependencies except xData (getData) or including a specific constraint on xData
    def __init__(self, dataPlotter, plt, dataName, independents, mainX = None, mainXdata = None):
        """
        dataName: (data name, unit)
        independents is a tuple of pairs: (independent name, unit)
        Main x data (if exists) is the independent to which the dependnet data is correlated,
        i.e. data[i] coressponds to x[i]
        mainX: (mainX name, unit)
        mainXdata: the main X data itself
        """
        self.dataName = dataName
        self.independentsList = independents
        if mainXdata is not None and mainX is None:
            raise Exception(" mainXdata is not None but mainX is None")
        self.mainX = mainX
        self.xData = mainXdata
        self.dataTable = {}
        self.dataPlotter = dataPlotter
        self.plt = plt
    
    def addMainXdata(self, xData):
        """Main x data is the independent to which the dependnet data is correlated,
        i.e. data[i] coressponds to x[i]
        """
        self.xData = xData 

    def addData(self, independents, data):
        if not len(independents)==len(self.independentsList):
            raise Exception("The number of independents is incorrect, it should be %d" % len(self.independentsList))
        self.dataTable[independents] = data
    
    def getData1d(self, independents):
        """
        Get the data constratining all independents to the given value (xData is unconstrained and is the x axis) 
        """
        if not len(independents)==len(self.independentsList):
            raise Exception("getData1d: The number of independents is incorrect, it should be %d" % len(self.independentsList))
        return self.dataTable[independents]

    def plotSingleData(self, independents, figure=None):
        """Plots data with given independents at given figure (or a new one if figure is None).
        (xData is unconstrained and is the x axis)
        Returns figure"""
        if figure is None:
            figure = self.plt.figure()
        else:
            self.plt.figure(figure.number)
        
        data = self.getData1d(independents)
        labelStringList = ["%s=%s [%s]" % (self.independentsList[i][0],str(independents[i]),self.independentsList[i][1]) for i in range(len(independents))]
        self.dataPlotter.plotData(self.plt, figure, self.mainX, self.xData, self.dataName, data, string.join(labelStringList,sep=", "))

        return figure

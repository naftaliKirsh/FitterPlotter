import string
import numpy as np

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
        self.independents_list = independents
        if mainXdata is not None and mainX is None:
            raise Exception(" mainXdata is not None but mainX is None")
        self.mainX = mainX
        self.xData = mainXdata
        self.data_table = {}
        self.dataPlotter = dataPlotter
        self.plt = plt
    
    def addMainXdata(self, xData):
        """Main x data is the independent to which the dependnet data is correlated,
        i.e. data[i] coressponds to x[i]
        """
        self.xData = xData 

    def addData(self, independents, data):
        if not len(independents)==len(self.independents_list):
            raise Exception("The number of independents is incorrect, it should be %d" % len(self.independents_list))
        self.data_table[independents] = data
    
    def getData1d(self, independents):
        """
        Get the data constratining all independents to the given value (xData is unconstrained and is the x axis) 
        """
        if not len(independents)==len(self.independents_list):
            raise Exception("getData1d: The number of independents is incorrect, it should be %d" % len(self.independents_list))
        return self.data_table[independents]
    
    def get_data_2d(self, constrained_independents, free_param_idx):
        """
        Get the data constratining all independents but the independent with index free_param_idx to the given value of constrained_independents 
        (xData is unconstrained and is the x axis). 
        returns the data and corresponding free independent value in a dict 
        """
        if not len(constrained_independents)==len(self.independents_list)-1:
            raise Exception("get_data_2d: The number of independents is incorrect, it should be %d" % len(self.independents_list)-1)
        
        # if type(free_param_idx)==str:
        #     free_param_idx = (zip(*self.independents_list)[0]).index(free_param_idx) #get index of free independent
        
        #create new dict with the free param values as key for ietms satisfing the constrains 
        data2d = {k[free_param_idx]:v for k,v in self.data_table.iteritems() if (k[:free_param_idx]+k[free_param_idx+1:])==constrained_independents}
        return data2d
        

    def plotSingleData(self, independents, figure=None):
        """Plots data with given independents at given figure (or a new one if figure is None).
        (xData is unconstrained and is the x axis)
        Returns figure"""
        if figure is None:
            figure = self.plt.figure()
        else:
            self.plt.figure(figure.number)
        
        data = self.getData1d(independents)
        labelStringList = ["%s=%s [%s]" % (self.independents_list[i][0],str(independents[i]),self.independents_list[i][1]) for i in range(len(independents))]
        self.dataPlotter.plotData(self.plt, figure, self.mainX, self.xData, self.dataName, data, string.join(labelStringList,sep=", "))

        return figure
    
    def plot_multiple_1d_data(self, constrained_independents, repeating_independent, figure=None):
        """Plots multiple 1d plots on the same figure.
        
        Args:
            constrained_independents: A tuple of values for the independents which are constrained (constant) for the data in the figure.
            repeating_independent: A string - the name of the indpendent which changes between different plots in the figure.

        Returns:
            A figure with the plots
        """

        if figure is None:
            figure = self.plt.figure()
        else:
            self.plt.figure(figure.number)

        repeating_param_idx = (zip(*self.independents_list)[0]).index(repeating_independent) #get index of free independent
        
        data_dict = self.get_data_2d(constrained_independents, repeating_param_idx)

        constrained_independents_idxes = range(repeating_param_idx)+range(repeating_param_idx+1,len(self.independents_list))
        title_str_list = ["%s=%s [%s]" % (self.independents_list[constrained_independents_idxes[i]][0],
            str(constrained_independents[i]),self.independents_list[constrained_independents_idxes[i]][1]) 
            for i in range(len(constrained_independents_idxes))]

        for param,data in data_dict.iteritems():
            label = "%s=%s [%s]" % (self.independents_list[repeating_param_idx][0],str(param),self.independents_list[repeating_param_idx][1])
            self.dataPlotter.plotData(self.plt, figure, self.mainX, self.xData, self.dataName, data, label, string.join(title_str_list,sep=", ")) 
        
        self.plt.legend()

        return figure
        
        
        


    
    def plot_2d_data(self, constrained_independents, free_independent, figure=None):
        """Plots data with given contstrains on all independents but one at given figure (or a new one if figure is None).
        xData is unconstrained and is the x axis, the y axis is the other unconstrained data 
        Returns figure"""
        if figure is None:
            figure = self.plt.figure()
        else:
            self.plt.figure(figure.number)

        free_param_idx = (zip(*self.independents_list)[0]).index(free_independent) #get index of free independent
        
        data_dict = self.get_data_2d(constrained_independents, free_param_idx)

        #sort the free param and data_list accordingly
        y_axis = data_dict.keys()
        data_list = data_dict.values()
        sorted_idxes = np.argsort(y_axis)
        y_axis = np.array(y_axis)[sorted_idxes]
        data_list = np.array(data_list)[sorted_idxes]
        #create data matrix
        data_matrix = np.matrix(data_list)

        self.dataPlotter.plot_data_2d(self.plt, figure, self.mainX, self.xData, self.independents_list[free_param_idx], 
            y_axis, self.dataName, data_matrix)
        
        return figure

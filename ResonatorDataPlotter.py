
import numpy as np

class ResonatorDataPlotter:
    def plotData(self, plt, figure, fDataName, fData, _, tData, label=None, title = None):
        """figure - figure to plot in
        fData - frequency data 
        tData - complex transmission data"""

        plt.figure(figure.number)
        plt.subplot(1,2,1)
        plt.plot(fData, 20*np.log10(np.abs(tData)), label=label)
        plt.xlabel("Frequency [%s]" % fDataName[1])
        plt.ylabel("Transmission [dB]")
        plt.subplot(1,2,2)
        plt.plot(np.real(tData), np.imag(tData), label=label)
        plt.xlabel("Re(t)")
        plt.ylabel("Im(t)")
        if title is not None:
            figure.suptitle(title)

    def plot_data_2d(self, plt, figure, f_data_name, f_data, y_data_name, y_data, _, t_matrix):
        """figure - figure to plot in
        f_data_name - ("Frequency",units) for frequency data
        f_data - frequency data 
        y_data_name - (data name,units) for y-axis data 
        y_data - y-axis data
        t_matrix - complex transmission data matrix"""

        plt.figure(figure.number)
        plt.imshow(20*np.log10(np.abs(t_matrix)),aspect="auto",extent=[f_data.min(), f_data.max(), y_data.min(), y_data.max()])
        plt.xlabel("Frequency [%s]" % f_data_name[1])
        plt.ylabel("%s [%s]" % (y_data_name[0],y_data_name[1]))
        plt.colorbar()

        


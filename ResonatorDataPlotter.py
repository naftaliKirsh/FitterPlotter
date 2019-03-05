
import numpy as np

class ResonatorDataPlotter:
    def plotData(self, plt, figure, fDataName, fData, _unused, tData, label=None):
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

        


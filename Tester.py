import numpy as np
import matplotlib.pyplot as plt
import Resonators.Utils as rutils
import FittingService as fs
import MatlabFitterWrapper as mfw
import MultiDataPlotter as mdp
import ResonatorDataPlotter as rdp


numBiases = 5
numPwrs = 5
f0Center = 6e3*1e6
f0s = f0Center+np.linspace(-10e3,10e3,numBiases) #Hz
Qs = 1e5*np.linspace(0.5, 1.5, numPwrs)
pwrs = np.linspace(0.5, 1.5, numPwrs)
biases  = np.linspace(-1,1,numBiases)
band = 0.4e6 #Hz
numPoints = 5000

freq = np.linspace(f0Center-band, f0Center+band, numPoints)

fittingService = fs.FittingService(mfw.MatlabFitterWrapper(False,False), (("Power","dBm"),("Bias","mA")), True)
resonatorDataPlotter = rdp.ResonatorDataPlotter()
multiDataPlotter = mdp.MultiDataPlotter(resonatorDataPlotter,plt,("Transmission",""),(("Power","dBm"),("Bias","mA")),("Frequency","MHz"))

multiDataPlotter.addMainXdata(freq/1e6)

for idx,power in enumerate(pwrs):
    for idx2,bias in enumerate(biases):
        tData = rutils.evalS21model(freq, [Qs[idx], f0s[idx2], 0, 0, 0, 1, 1, 0, 0.5, 0])
        fittingService.addMeasurement((power,bias), freq, tData)
        multiDataPlotter.addData((power,bias),tData)

fittingService.joinAllThreads()
print(fittingService.fitsTable)
print("----------")
# TODO - savable version : cPickle/json
pwrsList = set([x[0] for x in fittingService.fitsTable.keys()])
biasList = set([x[1] for x in fittingService.fitsTable.keys()])
# QList = [x["Q"] for x in fittingService.fitsTable.values()]

# plt.figure()
# plt.plot(pwrsList,QList,'*')
# plt.show()

for power in pwrsList:
    figure = plt.figure()
    for bias in biasList:
        multiDataPlotter.plotSingleData((power,bias),figure)
    plt.legend()
    plt.show()
    








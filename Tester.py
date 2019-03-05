import numpy as np
import matplotlib.pyplot as plt
import Resonators.Utils as rutils
import FittingService as fs
import MatlabFitterWrapper as mfw
import MultiDataPlotter as mdp
import ResonatorDataPlotter as rdp


f0 = 6e3*1e6 #Hz
Qs = 1e5*np.linspace(0.5, 1.5, 10)
pwrs = np.linspace(0.5, 1.5, 10)
# Qc = Qs[0]*2
band = 0.4e6 #Hz
numPoints = 5000

freq = np.linspace(f0-band, f0+band, numPoints)

fittingService = fs.FittingService(mfw.MatlabFitterWrapper(False,False), (("Power","dBm"),), True)
resonatorDataPlotter = rdp.ResonatorDataPlotter()
multiDataPlotter = mdp.MultiDataPlotter(resonatorDataPlotter,plt,("Transmission",""),(("Power","dBm"),),("Frequency","MHz"))

multiDataPlotter.addMainXdata(freq/1e6)

for idx,power in enumerate(pwrs):
    tData = rutils.evalS21model(freq, [Qs[idx], f0, 0, 0, 0, 1, 1, 0, 0.5, 0])
    fittingService.addMeasurement((power,), freq, tData)
    multiDataPlotter.addData((power,),tData)

fittingService.joinAllThreads()
print(fittingService.fitsTable)
print("----------")
# TODO - savable version : cPickle/json

pwrsList = [x[0] for x in fittingService.fitsTable.keys()]
QList = [x["Q"] for x in fittingService.fitsTable.values()]

plt.figure()
plt.plot(pwrsList,QList,'*')
plt.show()

figure = plt.figure()
for power in pwrsList:
    multiDataPlotter.plotSingleData((power,),figure)
plt.legend()
plt.show()










import Resonators.matlabFitter as mf
import matlab.engine

class MatlabFitterWrapper:

    def __init__(self, peakResonance, getTrailResonanceFromAbsData):
        self.peakResonance = peakResonance
        self.getTrailResonanceFromAbsData = getTrailResonanceFromAbsData
        print "Initializing Matlab..."
        self.matlabEngine = matlab.engine.start_matlab()

    def fit(self, freq, tData):
        fitResultsRaw = mf.performMatlabFit(self.matlabEngine, freq, tData, self.peakResonance, self.getTrailResonanceFromAbsData)

        return {"Q":fitResultsRaw[0][0][0],"f0":fitResultsRaw[0][0][1]}



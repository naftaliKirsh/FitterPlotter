import logging

class FittingService:
    def __init__(self, fitter, independents, fitAsync, debug=False):
        """TODO doc
                """
        if debug:
            logging.basicConfig(level=logging.DEBUG)

        self.fitter = fitter
        self.independents = independents
        self.fitsTable = {}
        self.fitAsync = fitAsync # TODO - implement
        if self.fitAsync:
            from threading import Thread, Lock 
            self.ThreadModule =  Thread 
            self.fitsTableLock = Lock()
            self.threadListLock = Lock()
            self.threadList = []

    def addMeasurement(self, independents, freq, tData):
        """TODO doc"""
        if not len(independents)==len(self.independents):
            raise Exception("The number of independents is incorrect, it should be %d" % len(self.independents))
        if self.fitAsync:
            thread = self.ThreadModule(target=self.addMeasurementAsync, args=(independents, freq, tData))
            with self.threadListLock:
                self.threadList.append(thread)
            thread.start()
        else:
            self.fitsTable[independents] = self.fitter.fit(freq, tData)
    
    def addMeasurementAsync(self, independents, freq, tData):
        logging.debug("Starting async fit\n")
        fitResults = self.fitter.fit(freq, tData)
        with self.fitsTableLock:
            self.fitsTable[independents] = fitResults
    
    def joinAllThreads(self):
        """Join all running threads"""

        if self.fitAsync:
            with self.threadListLock:
                for thread in self.threadList:
                    thread.join()
        else:
            return
    

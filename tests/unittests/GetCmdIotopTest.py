"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."


from backend.IOMonitor import IOMonitor

from tests.unittests.LepUnitTester import LepUnitTester

class GetCmdIotopTester(LepUnitTester):

    def __init__(self):

        LepUnitTester.__init__(self, 'GetCmdIotop')
        self.loadJson()
    
    def test(self):
        for sampleData in self.sampleDatas:
            self.report(sampleData)
            
            resultLines = self.getResultList(sampleData)
            for line in resultLines:
                print(line)

            monitor = IOMonitor('XXX')
            
            parsedData = monitor.getIoTopData(resultLines)
            self.pp.pprint(parsedData)

        

if( __name__ =='__main__' ):

    tester = GetCmdIotopTester()
    tester.test()
    
    
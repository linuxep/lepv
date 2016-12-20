"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from backend.CPUMonitor import CPUMonitor

from backend.tests.UnitTester import UnitTester

class GetProcCpuinfoTester(UnitTester):

    def __init__(self):

        UnitTester.__init__(self, 'GetProcCpuinfo')
        self.loadJson()
    
    def test(self):
        for sampleData in self.sampleDatas:
            self.report(sampleData)
            
            resultLines = self.getResultList(sampleData)
            for line in resultLines:
                print(line)

            monitor = CPUMonitor('www.readeeper.com')
            
            parsedData = monitor.getCpuInfo(resultLines)
            self.pp.pprint(parsedData)

        

if( __name__ =='__main__' ):

    tester = GetProcCpuinfoTester()
    tester.test()
    
    
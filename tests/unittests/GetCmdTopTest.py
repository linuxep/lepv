"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from backend.CPUMonitor import CPUMonitor

from tests.unittests.LepUnitTester import LepUnitTester


class GetCmdTopTester(LepUnitTester):

    def __init__(self):

        LepUnitTester.__init__(self, 'GetCmdTop')
        self.loadJson()
    
    def validate(self, parsedData):

        print("\n----------------------------------------------------\n")

        print("[Validating parsing result:]")
        self.validateBasics(parsedData)

        # self.lepAssertIn('processorsxxx', parsedData['data'], "processorsxxx was expected as a root element of result['data']")
        # 
        # self.assertEqual(True, 'processors' in parsedData['data'])
        # self.assertEqual(True, 'architecture' in parsedData['data'])
        # self.assertEqual(True, 'processorCount' in parsedData['data'])
        # 
        # for processorId in parsedData['data']['processors'].keys():
        #     self.assertEqual(True, self.isInteger(processorId))
        
    
    def test(self):
        for sampleData in self.sampleDatas:
            self.report(sampleData)
            
            resultLines = self.getResultList(sampleData)
            for line in resultLines:
                print(line)

            monitor = CPUMonitor('xxx')
            
            parsedData = monitor.getTopOutput(resultLines)
            self.pp.pprint(parsedData)
            
            self.validate(parsedData)

        

if( __name__ =='__main__' ):

    tester = GetCmdTopTester()
    tester.test()
    
    
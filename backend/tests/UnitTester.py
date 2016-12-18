"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import json
import os
import re
import pprint

class UnitTester:

    def __init__(self, lepdMethod):
        self.method = lepdMethod
        self.sampleDatas = None
        self.pp = pprint.PrettyPrinter(indent=2)

    def loadJson(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        fileName = os.path.basename(os.path.realpath(__file__))
    
        sampleDataFilePath = os.path.join(currentDir, self.method + ".json")
    
        with open(sampleDataFilePath) as data_file:
            jsonData = json.load(data_file)
            self.sampleDatas = jsonData['samples']
    
    def getResultList(self, sampleData):
        
        if (sampleData == None or 'result' not in sampleData):
            return []

        resultString = sampleData['result'].strip()
        lines = re.split(r'\\n|\n', resultString)
        return lines
    
    def report(self, sampleData):
        print("\r\n")
        print('-----------------------------------------------------------')
        print("Arch: " + sampleData['cpu'])
        print("Note: " + sampleData['note'])
        print('-----------------------------------------------------------')
        print('')
        
    
    def test(self):
        pass

if( __name__ =='__main__' ):

    tester = UnitTester()
    
    
"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import json
import pprint

class UnitTester:

    def __init__(self):
        pass

    def loadJson(self, jsonFilePath):
        with open(jsonFilePath) as data_file:
            return json.load(data_file)
    
    def getResultList(self, jsonFilePath):
        
        jsonData = self.loadJson(jsonFilePath)
        if (jsonData == None or 'result' not in jsonData):
            return []

        lines = jsonData['result'].strip().split("\n")
        for line in lines:
            print(line)

        return lines

if( __name__ =='__main__' ):

    tester = UnitTester()
    
    
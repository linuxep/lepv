"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import json
import os
import re
import pprint
import unittest

class LepUnitTester(unittest.TestCase):

    def __init__(self, lepdMethod):

        unittest.TestCase.__init__(self)
        
        self.method = lepdMethod
        self.sampleDatas = None
        self.pp = pprint.PrettyPrinter(indent=2)
        
    def loadJson(self):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        sampleDataFilePath = os.path.join(currentDir, 'sampleDatas', self.method + ".json")
    
        with open(sampleDataFilePath) as data_file:
            jsonData = json.load(data_file)
            self.sampleDatas = jsonData['samples']
    
    def getResultList(self, sampleData):
        
        if (sampleData == None or 'result' not in sampleData):
            return []

        resultString = sampleData['result'].strip()
        lines = re.split(r'\\n|\n', resultString)
        return lines


# assertEqual(a, b)	a == b
# assertNotEqual(a, b)	a != b
# assertTrue(x)	bool(x) is True
# assertFalse(x)	bool(x) is False
# assertIs(a, b)	a is b	2.7
# assertIsNot(a, b)	a is not b	2.7
# assertIsNone(x)	x is None	2.7
# assertIsNotNone(x)	x is not None	2.7
# assertIn(a, b)	a in b	2.7
# assertNotIn(a, b)	a not in b	2.7
# assertIsInstance(a, b)	isinstance(a, b)	2.7
# assertNotIsInstance(a, b)	not isinstance(a, b)	2.7

    def isInteger(self, val):
        try:
            int(val)
            return True
        except ValueError:
            return False

    def lepAssertIn(self, val, container, message):
        try:
            unittest.TestCase.assertIn(val, container)
        except:
            print(message)
    
    def validateBasics(self, parsedData):
        
        self.assertEqual(True, 'data' in parsedData)
    
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

    tester = LepUnitTester('')
    
    
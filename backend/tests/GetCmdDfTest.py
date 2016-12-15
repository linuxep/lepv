"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import json
import pprint

import os

from backend.tests.UnitTester import UnitTester

def testX86(sampleFilePath):

    tester = UnitTester()

    jsonData = ''
    with open(sampleFilePath) as data_file:
        jsonData = json.load(data_file)
    
    tester.getResultList(sampleFilePath)

def testArm(rawFile):
    filePath = os.path.join(rawFile, 'arm.txt')

    tester = UnitTester()
    tester.getResultList(filePath)

if( __name__ =='__main__' ):

    currentDir = os.path.dirname(os.path.realpath(__file__))
    fileName = os.path.basename(os.path.realpath(__file__))
    
    jsonFileName = fileName.replace(".py", ".json")
    
    rawDataPath = os.path.join(currentDir, jsonFileName)

    testX86(rawDataPath)
    
    
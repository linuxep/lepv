"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import json
import pprint

import os

from backend.LepDClient import LepDClient
from backend.tests.UnitTester import UnitTester


def testX86(rawFile):
    filePath = os.path.join(rawFile, 'x86.txt')

    tester = UnitTester()
    tester.getResultList(filePath)

def testArm(rawFile):
    filePath = os.path.join(rawFile, 'arm.txt')

    tester = UnitTester()
    tester.getResultList(filePath)

if( __name__ =='__main__' ):

    currentDir = os.path.dirname(os.path.realpath(__file__))
    
    rawDataPath = os.path.join(currentDir, "GetCmdIopp", 'raw')

    testX86(rawDataPath)
    
    
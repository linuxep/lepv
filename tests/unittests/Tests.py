"""Tests for LEPV"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import sys, inspect

__author__ = 'xmac'

class UnitTestManager():

    def __init__(self):
        
        # self.unitTestModule = sys.modules['tests.unittests.LepUnitTester']

        classmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        
        for classMember in classmembers:
            print(classMember)

    

if( __name__ =='__main__' ):
    
    testManager = UnitTestManager()
    
    






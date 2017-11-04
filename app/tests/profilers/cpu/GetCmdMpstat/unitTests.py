"""Tests for CPU profiler method: GetProcLoadavg"""
__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
from ddt import ddt, data, file_data, unpack
from pprint import pprint

from modules.profilers.cpu.CPUProfiler import CPUProfiler

@ddt
class GetCmdMpstatTestCase(unittest.TestCase):

    def setUp(self):
        self.profiler = CPUProfiler('')

    def describe(self, kernel, os, cpu, note):
        print(kernel)
        print(os)
        print(cpu)
        print(note)


    @file_data("unittests.json")
    def test(self, kernel, os, cpu, note, lepdResult, expected, expectedMatchType):
        self.describe(kernel, os, cpu, note)

        print(lepdResult)
        print(expectedMatchType)
        pprint(expected)


if( __name__ =='__main__' ):
    unittest.main()

"""Tests for CPU profiler method: GetProcLoadavg"""
from tests.profilers.cpu.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
from ddt import ddt, file_data
from pprint import pprint

from modules.profilers.cpu.CPUProfiler import CPUProfiler

@ddt
class GetCmdMpstatTestCase(LepvTestCase):

    def setUp(self):
        self.profiler = CPUProfiler('')

    @file_data("unittests.json")
    def test(self, kernel, os, cpu, note, lepdResult, expected, expectedMatchType):
        self.describe(kernel, os, cpu, note)

        actual = self.profiler.get_stat()
        print(expectedMatchType)
        pprint(expected)


if( __name__ =='__main__' ):
    unittest.main()

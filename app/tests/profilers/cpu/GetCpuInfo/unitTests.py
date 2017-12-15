"""Tests for CPU profiler method: GetCpuInfo"""
from modules.utils.dictUtil import DictUtil
from tests.profilers.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
from ddt import ddt, file_data
from pprint import pprint

from modules.profilers.cpu.CPUProfiler import CPUProfiler

@ddt
class GetProcLoadavgTestCase(LepvTestCase):

    def setUp(self):
        self.profiler = CPUProfiler('')

    def validate(self, expected, actual, expectedMatchType):

        print("Actual:")
        pprint(actual)

        compare_result = DictUtil.compare(actual, expected)

        if expectedMatchType == 'equals':
            self.assertEqual(compare_result, 0, "Expected and Actual does not match")
        elif expectedMatchType == 'contains':
            self.assertIn(compare_result, [0, 1], "Actual does not contain the expected")
        else:
            print("")


    @file_data("unittests.json")
    def test(self, kernel, os, cpu, note, lepdResult, expected, expectedMatchType):
        self.describe(kernel, os, cpu, note, expectedMatchType, expected)

        actual = self.profiler.get_processor_count(lepdResult)
        self.validate(expected, actual, expectedMatchType)


if( __name__ =='__main__' ):
    unittest.main()

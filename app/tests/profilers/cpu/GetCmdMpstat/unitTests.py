"""Tests for CPU profiler method: GetCmdMpstat"""
from app.modules.utils.dictUtil import DictUtil
from app.tests.profilers.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
from app.tests.jsondt import ddt, file_data
from pprint import pprint

from app.modules.profilers.cpu.CPUProfiler import CPUProfiler

@ddt
class GetCmdMpstatTestCase(LepvTestCase):

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
    def test(self, kernel, os, cpu, note, expectedMatchType, lepdResult, expected):
        self.describe(kernel, os, cpu, note, expectedMatchType, expected)

        actual = self.profiler.get_stat(lepdResult)
        self.validate(expected, actual, expectedMatchType)


if( __name__ =='__main__' ):
    unittest.main()

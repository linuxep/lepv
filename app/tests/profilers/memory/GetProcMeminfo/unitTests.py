from modules.profilers.memory.MemoryProfiler import MemoryProfiler
from modules.utils.dictUtil import DictUtil
from tests.profilers.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
from ddt import ddt, file_data
from pprint import pprint

@ddt
class GetProcMeminfoTestCase(LepvTestCase):

    def setUp(self):
        self.profiler = MemoryProfiler('')

    def validate(self, expected, actual, expected_match_type):

        print("Actual:")
        pprint(actual)

        compare_result = DictUtil.compare(actual, expected)

        if expected_match_type == 'equals':
            self.assertEqual(compare_result, 0, "Expected and Actual does not match")
        elif expected_match_type == 'contains':
            self.assertIn(compare_result, [0, 1], "Actual does not contain the expected")
        else:
            print("")


    @file_data("unittests.json")
    def test(self, kernel, os, cpu, note, lepdResult, expected, expected_match_type):
        self.describe(kernel, os, cpu, note, expected_match_type, expected)

        # getStatus -> GetProcMeminfo
        actual = self.profiler.getStatus(lepdResult)
        self.validate(expected, actual, expected_match_type)


if( __name__ =='__main__' ):
    unittest.main()

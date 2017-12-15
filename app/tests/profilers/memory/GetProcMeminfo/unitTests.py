from modules.profilers.memory.MemoryProfiler import MemoryProfiler
from tests.profilers.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
from ddt import ddt, file_data

@ddt
class GetProcMeminfoTestCase(LepvTestCase):

    def setUp(self):
        self.profiler = MemoryProfiler('')

    @file_data("unittests.json")
    def test(self, kernel, os, cpu, note, lepdResult, expected, expected_match_type):
        self.describe(kernel, os, cpu, note, expected_match_type, expected)

        # getStatus -> GetProcMeminfo
        actual = self.profiler.getStatus(lepdResult)
        self.validate(expected, actual, expected_match_type)


if __name__ == '__main__':
    unittest.main()

"""Tests for Memory profiler method: getProcrank"""
from modules.profilers.memory.MemoryProfiler import MemoryProfiler
from tests.profilers.lepvTestCase import LepvTestCase
import unittest
from ddt import ddt, file_data

from modules.profilers.io.IOProfiler import IOProfiler

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."


@ddt
class GetProcrankTestCase(LepvTestCase):

    def setUp(self):
        self.functor = MemoryProfiler('').getProcrank

    @file_data("unittests.json")
    def test(self, kernel, os, cpu, note, lepdResult, expected, expectedMatchType):
        self.unit_test(kernel, os, cpu, note, lepdResult, expected, expectedMatchType)

if __name__ == '__main__':
    unittest.main()

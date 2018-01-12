"""Tests for Perf profiler method: GetCmdPerfCpuclock"""
from tests.profilers.lepvTestCase import LepvTestCase
import unittest
from ddt import ddt, file_data

from app.modules.profilers.perf.PerfProfiler import PerfProfiler

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."


@ddt
class GetCmdPerfCpuclockTestCase(LepvTestCase):

    def setUp(self):
        self.functor = PerfProfiler('').get_perf_cpu_clock

    @file_data("unittests.json")
    def test(self, kernel, os, cpu, note, lepdResult, expected, expectedMatchType):
        self.unit_test(kernel, os, cpu, note, lepdResult, expected, expectedMatchType)


if __name__ == '__main__':
    unittest.main()

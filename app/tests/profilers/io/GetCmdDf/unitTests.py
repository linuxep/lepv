"""Tests for IO profiler method: get_capacity"""
from tests.profilers.lepvTestCase import LepvTestCase
import unittest
from ddt import ddt, file_data

from app.modules.profilers.io.IOProfiler import IOProfiler

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."


@ddt
class GetCmdDfTestCase(LepvTestCase):

    def setUp(self):
        self.functor = IOProfiler('').get_capacity

    @file_data("unittests.json")
    def test(self, kernel, os, cpu, note, lepdResult, expected, expectedMatchType):
        self.unit_test(kernel, os, cpu, note, lepdResult, expected, expectedMatchType)


if __name__ == '__main__':
    unittest.main()

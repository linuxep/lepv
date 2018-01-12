"""Tests for Perf profiler method: GetCmdPerfCpuclock"""
from app.modules.profilers.perf.flameBurner import FlameBurner
from app.modules.utils.dictUtil import DictUtil
from tests.profilers.lepvTestCase import LepvTestCase
import unittest
import json
from app.modules.profilers.perf.PerfProfiler import PerfProfiler

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."


class GetCmdPerfFlameTestCase(LepvTestCase):

    def setUp(self):
        self.profiler = PerfProfiler('')

    def test_flame_burner(self):
        with open('data/perf_script_output.txt') as perf_script_output_file:
            perf_script_output_lines = perf_script_output_file.readlines()

        with open('data/perf_script_burned_data.json') as burned_json_file:
            expected_burned_json = json.load(burned_json_file)

        burner = FlameBurner()
        actual_burned_data = burner.burn(perf_script_output_lines)

        compare_result = DictUtil.compare(expected_burned_json, actual_burned_data)
        self.assertEqual(compare_result, 0, "Expected and Actual does not match")


if __name__ == '__main__':
    unittest.main()

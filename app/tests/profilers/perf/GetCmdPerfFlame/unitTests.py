"""Tests for Perf profiler method: GetCmdPerfCpuclock"""
from modules.profilers.perf.flameBurner import FlameBurner
from modules.utils.dictUtil import DictUtil
from tests.profilers.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
import json
from ddt import ddt, file_data
from pprint import pprint

from modules.profilers.perf.PerfProfiler import PerfProfiler

@ddt
class GetCmdPerfFlameTestCase(LepvTestCase):

    def setUp(self):
        self.profiler = PerfProfiler('')

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

    # def test_burn_data(self):
    #     with open('perf_script_output.txt') as perf_script_output_file:
    #         perf_script_output_lines = perf_script_output_file.readlines()
    #
    #     with open('perf_script_burned_data.json') as burned_json_file:
    #         expected_burned_json = json.load(burned_json_file)
    #
    #     actual_burned_data = self.profiler.get_cmd_perf_flame(perf_script_output_lines)
    #
    #     compare_result = DictUtil.compare(expected_burned_json, actual_burned_data)
    #     self.assertEqual(compare_result, 0, "Expected and Actual does not match")


    def test_flame_burner(self):
        with open('perf_script_output.txt') as perf_script_output_file:
            perf_script_output_lines = perf_script_output_file.readlines()

        with open('perf_script_burned_data.json') as burned_json_file:
            expected_burned_json = json.load(burned_json_file)

        burner = FlameBurner()
        actual_burned_data = burner.burn(perf_script_output_lines)

        compare_result = DictUtil.compare(expected_burned_json, actual_burned_data)
        self.assertEqual(compare_result, 0, "Expected and Actual does not match")




if( __name__ =='__main__' ):
    unittest.main()

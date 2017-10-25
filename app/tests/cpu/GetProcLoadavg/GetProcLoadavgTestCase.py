"""Tests for CPU profiler method: GetProcLoadavg"""
__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest

from modules.profilers.cpu.CPUProfiler import CPUProfiler


class GetProcLoadavgTestCase(unittest.TestCase):

    def setUp(self):
        self.profiler = CPUProfiler('')

    def describe(self, test_data):
        for test_data_key in test_data:
            if test_data_key == 'lepdResult':
                continue
            if test_data_key == 'expected':
                continue

            print(test_data_key + ": " + test_data[test_data_key])

    def doPositiveTest(self, test_data):
        self.describe(test_data)

        actual_result = self.profiler.get_average_load(test_data['lepdResult'])

        # self.assertTrue(isinstance(count, int), "CPU processor count '%s' is not an integer" % count)
        self.assertTrue(actual_result, "Result should NOT be null")

        self.assertIn('data', actual_result, "field 'data' should present")

        actualData = actual_result['data']
        self.assertIn('last1', actualData, "'last1' should present in 'data'")
        self.assertEqual(str(test_data['expected']['data']['last1']), str(actualData['last1']), "'last1' values do NOT match!")

        self.assertIn('last5', actualData, "'last5' should present in 'data'")
        self.assertEqual(str(test_data['expected']['data']['last5']), str(actualData['last5']), "'last5' values do NOT match!")

        self.assertIn('last15', actualData, "'last15' should present in 'data'")
        self.assertEqual(str(test_data['expected']['data']['last15']), str(actualData['last15']), "'last15' values do NOT match!")

    def testGoldenPass(self):

        test_data = {
          "kernel": "",
          "os": "linux",
          "cpu": "x86",
          "note": "data from www.rmlink.cn",
          "lepdResult":	"0.18 0.19 0.12 1/77 11132\nlepdendstring",
          "expected": {
            "data": {
              "last1": 0.18,
              "last5": 0.19,
              "last15": 0.12
            }
          }
        }

        self.doPositiveTest(test_data)


    def testGoldenPassForX86(self):

        test_data = {
          "kernel": "",
          "os": "linux",
          "cpu": "x86",
          "note": "data from www.rmlink.cn",
          "lepdResult":	"0.18 0.79 0.92 1/77 11132\nlepdendstring",
          "expected": {
            "data": {
              "last1": 0.18,
              "last5": 0.79,
              "last15": 0.92
            }
          }
        }

        self.doPositiveTest(test_data)

if( __name__ =='__main__' ):
    unittest.main()

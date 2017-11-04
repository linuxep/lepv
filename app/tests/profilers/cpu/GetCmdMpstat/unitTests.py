"""Tests for CPU profiler method: GetProcLoadavg"""
__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest

from modules.profilers.cpu.CPUProfiler import CPUProfiler


class GetCmdMpstatTestCase(unittest.TestCase):

    def setUp(self):
        self.profiler = CPUProfiler('')

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


if( __name__ =='__main__' ):
    unittest.main()

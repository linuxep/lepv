"""Tests for Perf profiler method: GetCmdPerfCpuclock"""
import pprint

from modules.profilers.perf.flameBurner import FlameBurner
from modules.utils.dictUtil import DictUtil
from tests.profilers.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest

from modules.profilers.perf.PerfProfiler import PerfProfiler

class FlameGraphTestCase(LepvTestCase):

    def setUp(self):
        self.profiler = PerfProfiler('www.rmlink.cn')
        self.burner = FlameBurner()

    def testAgainstOfficialSVG(self):
        print("Get perf script output")

        lepd_command = 'GetCmdPerfFlame'
        response_lines = self.profiler.client.getResponse(lepd_command)

        for line in response_lines:
            print(line)

        burned_json = self.burner.burn(response_lines)
        pprint.pprint(burned_json)













if( __name__ =='__main__' ):
    unittest.main()

"""Tests for Perf profiler method: GetCmdPerfCpuclock"""
from modules.profilers.perf.flameBurner import FlameBurner
from modules.utils.dictUtil import DictUtil
from tests.profilers.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
import json
from pprint import pprint

from modules.profilers.perf.PerfProfiler import PerfProfiler


class GetCmdPerfFlameComponentTestCase(unittest.TestCase):

    def setUp(self):
        self.profiler = PerfProfiler('www.rmlink.cn')

    def test_flame_burner(self):

        flame_data = self.profiler.get_cmd_perf_flame()

        pprint(flame_data)


if( __name__ =='__main__' ):
    unittest.main()

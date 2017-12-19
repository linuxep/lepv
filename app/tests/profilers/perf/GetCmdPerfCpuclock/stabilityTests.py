from tests.profilers.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest

from modules.profilers.perf.PerfProfiler import PerfProfiler


class StabilityTestCase(LepvTestCase):

    def setUp(self):
        pass

    def validate(self, actual):
        pass

    def test_stability(self):
        profiler = PerfProfiler('www.rmlink.cn')
        self.repeated_test(profiler.get_perf_cpu_clock)


if __name__ =='__main__':
    unittest.main()

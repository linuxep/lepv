from tests.profilers.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest

from app.modules.profilers.memory.MemoryProfiler import MemoryProfiler


class StabilityTestCase(LepvTestCase):

    def setUp(self):
        pass

    def validate(self, actual):
        pass

    def test_stability(self):
        profiler = MemoryProfiler('www.rmlink.cn')
        self.repeated_test(profiler.getStatus)


if __name__ =='__main__':
    unittest.main()

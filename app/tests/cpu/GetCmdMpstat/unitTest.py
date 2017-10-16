"""Module for CPU related data parsing Testing"""
__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
from ddt import ddt, data, file_data, unpack

from modules.cpu.CPUProfiler import CPUProfiler

@ddt
class CpuProfilerTest(unittest.TestCase):

    def setUp(self):
        self.server = 'www.rmlink.cn'
        self.profiler = CPUProfiler(self.server)

    def test_getCpuCount(self):

        returnedData = self.profiler.getProcessorCount()

        self.assertIn('count', returnedData, "'count' is not a key in the returned object")

        count = returnedData['count']
        self.assertTrue(isinstance(count, int), "CPU processor count '%s' is not an integer" % count)

    @file_data("try.json")
    @unpack
    def test_parsing(self, test_case):
        print(test_case)


if( __name__ =='__main__' ):
    suite = unittest.TestLoader().loadTestsFromTestCase(CpuProfilerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

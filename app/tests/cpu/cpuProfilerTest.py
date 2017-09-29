"""Module for CPU related data parsing Testing"""
__author__    = "Copyright (c) 2017, Marin Software>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest

from modules.cpu.CPUProfiler import CPUProfiler


class CpuProfilerTest(unittest.TestCase):

    def setUp(self):
        self.server = 'www.linuxxueyuan.com'
        self.profiler = CPUProfiler(self.server)

    def test_getCpuCount(self):

        returnedData = self.profiler.getProcessorCount()

        self.assertIn('count', returnedData, "'count' is not a key in the returned object")

        count = returnedData['count']
        self.assertTrue(isinstance(count, int), "CPU processor count '%s' is not an integer" % count)


if( __name__ =='__main__' ):
    unittest.main()

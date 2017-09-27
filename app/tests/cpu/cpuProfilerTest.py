"""Module for CPU related data parsing Testing"""
__author__    = "Copyright (c) 2017, Marin Software>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest

from app.modules.cpu.CPUProfiler import CPUProfiler


class CpuTest(unittest.TestCase):

    def setUp(self):
        self.server = 'www.linuxxueyuan.com'
        self.profiler = CPUProfiler(self.server)

    def test_getCpuCount(self):

        cpuCountData = self.profiler.getProcessorCount()

        self.assertTrue(cpuCountData, "XXXXXXX")


if( __name__ =='__main__' ):
    unittest.main()

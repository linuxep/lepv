import re

import time

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

from pprint import pprint
import unittest
import timeit


class LepvTestCase(unittest.TestCase):

    def describe(self, kernel, os, cpu, note, expected_match_type, expected_data):
        print("")
        print("KERNEL:         " + kernel)
        print("OS:             " + os)
        print("CPU:            " + cpu)
        print("NOTE:           " + note)
        print("Match Type:     " + expected_match_type)
        print("")
        print("Expected Data:  ")
        pprint(expected_data)
        print("")

    def get_functor_info(self, functor):
        #<bound method MemoryProfiler.getStatus of <modules.profilers.memory.MemoryProfiler.MemoryProfiler object at 0x101515e10>>
        reg = re.search('<bound method (.*) of <.*', str(functor), re.IGNORECASE)
        if reg:
            return reg.group(1)

        return str(functor)

    def repeated_test(self, functor, repeat_count=50):

        i = 1
        while i <= repeat_count:
            print('[' + str(i) + ']: ' + self.get_functor_info(functor))
            i += 1

            start = time.time()
            data = functor()
            end = time.time()

            time_used = end - start
            time_used = "{0:.2f}".format(round(time_used,2))
            print('     [' + str(time_used) + '] seconds to finish')

            self.validate(data)




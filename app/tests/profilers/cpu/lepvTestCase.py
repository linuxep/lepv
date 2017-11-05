__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest


class LepvTestCase(unittest.TestCase):

    def describe(self, kernel, os, cpu, note):
        print(kernel)
        print(os)
        print(cpu)
        print(note)

    def compare_dicts(self, dict_first, dict_second):

        return 0

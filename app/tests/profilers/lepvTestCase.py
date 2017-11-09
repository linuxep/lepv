__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

from pprint import pprint
import unittest


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

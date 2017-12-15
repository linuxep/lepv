import re

import time

from modules.utils.dictUtil import DictUtil

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

    def unit_test(self, kernel, os, cpu, note, lepdResult, expected, expectedMatchType):
        self.describe(kernel, os, cpu, note, expectedMatchType, expected)

        actual = self.functor(lepdResult)
        self.validate(expected, actual, expectedMatchType)

    def validate_schema(self, data):
        print(data)

    def validate(self, expected, actual, expectedMatchType):

        print("Actual:")
        pprint(actual)

        compare_result = DictUtil.compare(actual, expected)

        if expectedMatchType == 'equals':
            self.assertEqual(compare_result, 0, "Expected and Actual does not match")
        elif expectedMatchType == 'contains':
            self.assertIn(compare_result, [0, 1], "Actual does not contain the expected")
        else:
            print("")

    def get_functor_info(self, functor):
        reg = re.search('<bound method (.*) of <.*', str(functor), re.IGNORECASE)
        if reg:
            return reg.group(1)

        return str(functor)

    def repeated_test(self, functor, repeat_count=50):

        i = 1
        while i <= repeat_count:
            print('\n[' + str(i) + ']: ' + self.get_functor_info(functor))
            i += 1

            start = time.time()
            data = functor()
            end = time.time()

            time_used = end - start
            time_used = "{0:.2f}".format(round(time_used,2))
            print('     [' + str(time_used) + '] seconds to finish')

            self.validate_schema(data)




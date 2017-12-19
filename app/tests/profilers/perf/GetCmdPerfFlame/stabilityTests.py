from tests.profilers.lepvTestCase import LepvTestCase

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest

from modules.profilers.perf.PerfProfiler import PerfProfiler


class StabilityTestCase(LepvTestCase):

    def validate_schema(self, data):
        # print(data)
        if 'flame' not in data:
            print("      'flame' should be a root property of the response")
            print("     Failed!")
            return

        if len(data['flame']) == 0:
            print("      flame data not constructed")
            print("perf script outputs:")
            print("\n-------------------------------------------")
            for line in data['perf_script_output']:
                print(line)
            print("-------------------------------------------\n")

            print("     Failed!")
            return

        print("     Succeeded!")

    def test_stability(self):
        profiler = PerfProfiler('www.rmlink.cn')
        self.repeated_test(profiler.get_cmd_perf_flame)


if __name__ =='__main__':
    unittest.main()

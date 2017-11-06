from modules.utils.dictUtil import DictUtil

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest


class DictCmpTests(unittest.TestCase):

    def test_two_flat_dicts_equal(self):

        dict_1 = {
            "project": "lepv"
        }

        dict_2 = {
            "project": "lepv"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 0, 'the comparison result of two identical flat dicts should be 0')


if __name__ =='__main__':
    unittest.main()
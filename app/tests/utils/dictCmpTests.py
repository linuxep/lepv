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

        dict_3 = {}

        dict_4 = {}

        comp_result_1 = DictUtil.compare(dict_1, dict_2)
        comp_result_2 = DictUtil.compare(dict_3, dict_4)
        self.assertEqual(comp_result_1, 0, 'the comparison result of two identical flat dicts should be 0')
        self.assertEqual(comp_result_2, 0, 'the comparison result of two identical flat dicts should be 0')

    def test_two_flat_dicts_contains(self):
        
        dict_1 = {
            "project1": "lepv1",
            "project2": "lepv2"
        }
        
        dict_2 = {
            "project1": "lepv1",
            "project2": "lepv2", 
            "project3": "lepv3"
        }

        dict_3 = {
            "project1": {"k1": "v1"},
            "project2": "lepv2"
        }

        dict_4 = {
            "project1": {"k1": "v1", "k2": "v2"},
            "project2": "lepv2"
        }

        comp_result_1 = DictUtil.compare(dict_2, dict_1)
        comp_result_2 = DictUtil.compare(dict_4, dict_3)
        self.assertEqual(comp_result_1, 1, 'the comparison result of two identical flat dicts should be 1')
        self.assertEqual(comp_result_2, 1, 'the comparison result of two identical flat dicts should be 1')

    def test_two_flat_dicts_contained(self):
        
        dict_1 = {
            "project1": {"k1": "v1"},
            "project2": "lepv2"
        }

        dict_2 = {
            "project1": {"k1": "v1", "k2": "v2"},
            "project2": "lepv2"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, -1, 'the comparison result of two identical flat dicts should be -1')

    def test_two_flat_dicts_other(self):

        dict_1 = {
            "project1": "lepv1",
            "project2": "lepv2"
        }
        
        dict_2 = {
            "project1": "lepv2",
            "project2": "lepv1", 
        }

        dict_3 = {
            "project1": {"k1": "v1"},
            "project2": "lepv2"
        }

        dict_4 = {
            "project1": {"k1": "v2", "k2": "v1"},
            "project2": "lepv2"
        }

        comp_result_1 = DictUtil.compare(dict_1, dict_2)
        comp_result_2 = DictUtil.compare(dict_3, dict_4)
        self.assertEqual(comp_result_1, 2, 'the comparison result of two identical flat dicts should be 2')
        self.assertEqual(comp_result_2, 2, 'the comparison result of two identical flat dicts should be 2')


if __name__ =='__main__':
    unittest.main()

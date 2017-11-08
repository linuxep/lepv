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

    def test_two_empty_dicts_should_equal(self):
        
        dict_1 = {}
        dict_2 = {}

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 0, 'the comparison result of two empty dicts should be 0')

    def test_empty_dict_being_contained(self):
        dict_1 = {
            "project": "lepv"
        }
        dict_2 = {}

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 1, 'empty dict should be considered "contained" by any non-empty dict')

    def test_two_null_dicts_should_equal(self):
        dict_1 = None
        dict_2 = None

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 0, 'the comparison result of two null dicts should be 0')

    def test_two_flat_dicts_contains(self):
        
        dict_1 = {
            "project1": "lepv1",
            "project2": "lepv2",
            "project3": "lepv3"
        }
        
        dict_2 = {
            "project1": "lepv1",
            "project2": "lepv2"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 1, 'if the first dict contains second, the result should be 1')

    def test_two_deep_dicts_contains(self):

        dict_1 = {
            "project1": {
                "k1": "v1",
                "k2": "v2"
            },
            "project2": "lepv2"
        }

        dict_2 = {
            "project1": {
                "k1": "v1"
            },
            "project2": "lepv2"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 1, 'The first deep dict contains second, the result should be 1')

    def test_two_dicts_contained(self):
        
        dict_1 = {
            "project1": {"k1": "v1"},
            "project2": "lepv2"
        }

        dict_2 = {
            "project1": {"k1": "v1", "k2": "v2"},
            "project2": "lepv2"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, -1, 'if the second dict contains the first, the result should be -1')

    def test_two_dicts_not_equal_not_contains_not_contained(self):

        dict_1 = {
            "project1": {"k1": "v1"},
            "project2": "lepv2"
        }

        dict_2 = {
            "project": {"k1": "v2222", "k2": "v1"},
            "project2": "lepv2"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 2, 'if there is no inclusion relationship, the result should be 2')


if __name__ =='__main__':
    unittest.main()

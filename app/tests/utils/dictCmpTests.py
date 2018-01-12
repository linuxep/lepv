from app.modules.utils.dictUtil import DictUtil

__author__    = "Copyright (c) 2017, LEP>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
import json


class DictCmpTests(unittest.TestCase):
        
    def test_compare_two_flat_dicts_equal(self):

        dict_1 = {
            "project": "lepv"
        }

        dict_2 = {
            "project": "lepv"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 0, 'The comparison result of two identical flat dicts should be 0')

    def test_compare_two_empty_dicts_should_equal(self):
        
        dict_1 = {}
        dict_2 = {}

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 0, 'The comparison result of two empty dicts should be 0')

    def test_compare_empty_dict_being_contained(self):
        dict_1 = {
            "project": "lepv"
        }
        dict_2 = {}

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 1, 'Empty dict should be considered "contained" by any non-empty dict')

    def test_compare_two_null_dicts_should_equal(self):
        dict_1 = None
        dict_2 = None

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 0, 'The comparison result of two null dicts should be 0')

    def test_compare_two_flat_dicts_contains(self):
        
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
        self.assertEqual(comp_result, 1, 'If the first flat dict contains the second, the result should be 1')

    def test_compare_two_deep_dicts_contains(self):

        dict_1 = {
            "project1": {"k1": "v1", "k2": "v2"},
            "project2": "lepv2"
        }

        dict_2 = {
            "project1": {"k1": "v1" },
            "project2": "lepv2"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 1, 'If the first deep dict contains the second, the result should be 1')

    def test_compare_two_deep_dicts_with_list_contains(self):

        dict_actual = {
            "data1": [
              {
                "Overhead": "45.17%",
                "Command": "uwsgi",
                "Shared Object": "libpython3.5m.so.1.0",
                "Symbol": "[.] 0x000000000011c525"
              },
              {
                "Overhead": "1.25%",
                "Command": "uwsgi",
                "Shared Object": "_socket.cpython-35m-x86_64-linux-gnu.so",
                "Symbol": "[.] 0x0000000000006b00"
              }
            ],
            "data2": "lepv"
        }

        dict_expected = {
            "data1": [
                {
                    "Overhead": "45.17%",
                    "Command": "uwsgi",
                    "Shared Object": "libpython3.5m.so.1.0",
                    "Symbol": "[.] 0x000000000011c525"
                }
            ],
        }

        comp_result = DictUtil.compare(dict_actual, dict_expected)
        self.assertEqual(comp_result, 1, 'If the first deep dict with list contains the second, the result should be 1')

    def test_compare_two_flat_dicts_contained(self):
        
        dict_1 = {
            "project1": "lepv1",
            "project2": "lepv2"
        }

        dict_2 = {
            "project1": "lepv1",
            "project2": "lepv2",
            "project3": "lepv3"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, -1, 'If the second flat dict contains the first, the result should be -1')

    def test_compare_two_deep_dicts_contained(self):
        
        dict_1 = {
            "project1": {"k1": "v1"},
            "project2": "lepv2"
        }

        dict_2 = {
            "project1": {"k1": "v1", "k2": "v2"},
            "project2": "lepv2"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, -1, 'If the second deep dict contains the first, the result should be -1')

    def test_compare_two_deep_dicts_with_list_contained(self):

        dict_actual = {
            "data1": [
                {
                    "Overhead": "45.17%",
                    "Command": "uwsgi",
                    "Shared Object": "libpython3.5m.so.1.0",
                    "Symbol": "[.] 0x000000000011c525"
                }
            ],
        }

        dict_expected = {
            "data1": [
              {
                "Overhead": "45.17%",
                "Command": "uwsgi",
                "Shared Object": "libpython3.5m.so.1.0",
                "Symbol": "[.] 0x000000000011c525"
              },
              {
                "Overhead": "1.25%",
                "Command": "uwsgi",
                "Shared Object": "_socket.cpython-35m-x86_64-linux-gnu.so",
                "Symbol": "[.] 0x0000000000006b00"
              }
            ],
            "data2": "lepv"
        }

        comp_result = DictUtil.compare(dict_actual, dict_expected)
        self.assertEqual(comp_result, -1, 'If the second deep dict with list contains the first, the result should be -1')
    
    def test_compare_two_flat_dicts_not_equal_not_contains_not_contained(self):

        dict_1 = {
            "project1": "lepv1",
            "project2": "lepv2"
        }

        dict_2 = {
            "project3": "lepv3",
            "project4": "lepv4"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 2, 'If two flat dicts are no inclusion relationship, the result should be 2')    
        
    def test_compare_two_deep_dicts_not_equal_not_contains_not_contained(self):

        dict_1 = {
            "project1": {"k1": "v1"},
            "project2": "lepv2"
        }

        dict_2 = {
            "project1": {"k1": "v2", "k2": "v1"},
            "project2": "lepv2"
        }

        comp_result = DictUtil.compare(dict_1, dict_2)
        self.assertEqual(comp_result, 2, 'If two deep dicts are no inclusion relationship, the result should be 2')    

    def test_compare_two_deep_dicts_with_list_not_equal_not_contains_not_contained(self):
        
        dict_actual = {
            "data1": [
             {
                "Overhead": "45.17%",
                "Command": "uwsgi",
                "Shared Object": "libpython3.5m.so.1.0",
                "Symbol": "[.] 0x000000000011c525"
             },
            ],
            "data2": "lepv"
        }

        dict_expected = {
            "data1": [
             {
                "Overhead": "1.25%",
                "Command": "uwsgi",
                "Shared Object": "_socket.cpython-35m-x86_64-linux-gnu.so",
                "Symbol": "[.] 0x0000000000006b00"
             }
            ],
            "data2": "lepv"
        }

        comp_result = DictUtil.compare(dict_actual, dict_expected)
        self.assertEqual(comp_result, 2, 'If two deep dicts with list are no inclusion relationship, the result should be 2')

    def test_compare_two_deep_dicts_with_arrays(self):
        with open('./dict_data/a.json') as json_file:
            expected_json = json.load(json_file)

        with open('./dict_data/b.json') as json_file:
            same_json = json.load(json_file)

        comp_result = DictUtil.compare(expected_json, same_json)
        self.assertEqual(comp_result, 0, 'Two identical dicts with deep arrays should equal')



    # def test_locate_child_node_for_dict_by_property(self):
    #     dict = {
    #             "name": "root",
    #             "value": 8,
    #             "children": [
    #                 {
    #                     "name": "x86_64_start_kernel",
    #                     "value": 4,
    #                     "children": [
    #                         {
    #                         "name": "x86_64_start_reservations",
    #                         "value": 2,
    #                         "children": []
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #
    #     property_key = 'name'
    #     property_value = 'root'
    #     located_node = DictUtil.locate_node_by_property_value(dict, property_key, property_value)
    #
    #     comp_result = DictUtil.compare(dict, located_node)
    #     self.assertEqual(comp_result, 0, 'The root dict should be located and returned')
    #
    #
    # def test_locate_child_node_for_array_by_property(self):
    #     dict = {
    #             "name": "root",
    #             "value": 8,
    #             "children": [
    #                 {
    #                     "name": "x86_64_start_kernel",
    #                     "value": 4,
    #                     "children": [
    #                         {
    #                             "name": "x86_64_start_reservations",
    #                             "value": 2,
    #                             "children": []
    #                         }
    #                     ]
    #                 },
    #
    #                 {
    #                     "name": "x86_64_start_kernel_XXXX",
    #                     "value": 3,
    #                     "children": [
    #                         {
    #                             "name": "x86_64_start_reservations_XXX",
    #                             "value": 2,
    #                             "children": []
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #
    #     property_key = 'name'
    #     property_value = 'x86_64_start_kernel_XXXX'
    #     located_node = DictUtil.locate_node_by_property_value(dict['children'], property_key, property_value)
    #
    #     expected_node = {
    #                         "name": "x86_64_start_kernel_XXXX",
    #                         "value": 3,
    #                         "children": [
    #                             {
    #                                 "name": "x86_64_start_reservations_XXX",
    #                                 "value": 2,
    #                                 "children": []
    #                             }
    #                         ]
    #                     }
    #
    #     comp_result = DictUtil.compare(located_node, expected_node)
    #     self.assertEqual(comp_result, 0, 'The dict in the array should be located and returned')

if __name__ =='__main__':
    unittest.main()


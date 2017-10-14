"""Module for CPU related data parsing Testing"""
__author__    = "Copyright (c) 2017, Marin Software>"
__copyright__ = "Licensed under GPLv2 or later."

import unittest
import requests


class CpuAPITest(unittest.TestCase):

    def setUp(self):
        self.server = 'www.linuxep.com'
        self.apiPrefix = '/api/cpu'

    # /api/cpu/count
    def test_getCpuCount(self):

        url = self.apiPrefix + 'count' + '/' + self.server

        jsonResponse = {}
        try:
            response = requests.get(url)
            jsonResponse = response.json()
        except:
            print("Failed in getting response")

        self.assertTrue(jsonResponse, "XXXXXXX")


if( __name__ =='__main__' ):
    unittest.main()

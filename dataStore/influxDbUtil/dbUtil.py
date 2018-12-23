"""Core module for interacting with influxDB"""

__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from influxdb import InfluxDBClient

'''
MyInfluxDbClient is the warpper of InfluxDBClient,
To insert data and  to query data can use it
'''


class MyInfluxDbClient:
    def __init__(self, influxDBAddress,port=8086,username='root',password='',database="lep"):
        self._client = InfluxDBClient(influxDBAddress, port,username,password,database)

    def write_points(self,  json_body):

        if self._client.write_points(json_body):
            return True
        else:
            return False

    def query(self, statement):
        return self._client.query(statement)

"""Core module for interacting with influxDB"""

__author__ = "李旭升 <programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from influxdb import InfluxDBClient

'''
myInfluxDbClient是自己封装的InfluxDBClient,
为了插入和读取InfluxDB
'''


class myInfluxDbClient:
    def __init__(self, influxDBAddress):
        self._client = InfluxDBClient(influxDBAddress, 8086, 'root', ",", "lep")

    def write_points(self, server, json_body):

        if self._client.write_points(json_body):
            return True
        else:
            return False

    def query(self, statement):
        return self._client.query(statement)

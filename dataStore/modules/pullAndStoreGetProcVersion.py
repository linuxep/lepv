__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetProcVersion from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetProcVersion(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetProcVersion')
    mystr = res['result']

    json_body = [
        {
            "measurement": "GetProcVersion",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "LinuxVersion": mystr
            }
        }
    ]

    influxDbClient.write_points(json_body)

if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetProcVersion(lepdClient, influxDbClient)
        time.sleep(1)

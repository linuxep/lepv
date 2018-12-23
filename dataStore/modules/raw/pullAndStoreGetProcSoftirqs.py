__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetProcSoftirqs from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetProcSoftirqs(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetProcSoftirqs')
    # print(res)
    # str1 = res["result"].split("\n")
    # for x in str1:
    #     print(x)
    json_body = [
        {
            "measurement": "GetProcSoftirqs",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "softirqs": res["result"]
            }
        }
    ]

    influxDbClient.write_points(json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetProcSoftirqs(lepdClient, influxDbClient)
        time.sleep(1)

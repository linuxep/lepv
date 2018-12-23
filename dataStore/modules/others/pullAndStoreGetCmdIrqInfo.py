__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetCmdDmesg from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdIrqInfo(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdIrqInfo')
    print(res)
    str1 = res["result"].split(" ")
    x1=str1[0].split(":")
    x2=x1[1].split("/")
    x3=x2[0]
    print(x3)
    y1=str1[1].split(":")
    y2=y1[1].split("/")
    y3=y2[0]
    print(y3)

    json_body = [
        {
            "measurement": "GetCmdIrqInfo",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "irq": int(x3),
                "softirq": int(y3)
            }
        }
    ]

    influxDbClient.write_points(json_body)



if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetCmdIrqInfo(lepdClient, influxDbClient)
        time.sleep(1)

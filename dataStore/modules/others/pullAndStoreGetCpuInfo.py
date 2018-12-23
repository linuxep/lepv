__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetCpuInfo from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCpuInfo(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCpuInfo')
    # print(res)
    str1 = res["result"].split("\n")
    data1 = str1[0].split(": ")
    data2 = str1[1].split(": ")
    # for x in data1:
    #     print(x)
    # for x in data2:
    #     print(x)
    json_body = [
        {
            "measurement": "GetCpuInfo",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "cpunr": int(data1[1]),
                "cpu_name": data2[1]

            }
        }
    ]

    influxDbClient.write_points(json_body)



if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetCpuInfo(lepdClient, influxDbClient)
        time.sleep(1)

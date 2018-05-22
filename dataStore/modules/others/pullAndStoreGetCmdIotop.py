__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient
import re

import time

'''
fetch data related to  GetCmdIrqInfo from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdIotop(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdIotop')
    # print(res)

    str1 = res["result"].split("\n")

    data=re.findall(r"\d+\.?\d*", str1[0])

    # print(data)
    json_body = [
        {

            "measurement": "GetCmdIotop",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "Total_DISK_READ": float(data[0]),
                "Total_DISK_WRITE": float(data[1])
            }
        }
    ]

    influxDbClient.write_points(json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(120):
        pullAndStoreGetCmdIotop(lepdClient, influxDbClient)
        # time.sleep(0.3)

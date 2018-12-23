__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time
import re

'''
fetch data related to  GetCmdProcrank from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdProcrank(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdProcrank')
    print(res)
    str1 = res["result"].split("\n")
    # for x in str1:
    #     print(x)
    # print(str1[-2])

    data = re.findall(r"\d+\.?\d*", str1[-2])
    print(data)

    json_body = [
        {
            "measurement": "GetCmdProcrank",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "total": int(data[0]),
                "free": int(data[1]),
                "buffers": int(data[2]),
                "cached": int(data[3]),
                "shmem": int(data[4]),
                "slab": int(data[5])

            }
        }
    ]

    influxDbClient.write_points(json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetCmdProcrank(lepdClient, influxDbClient)
        time.sleep(1)

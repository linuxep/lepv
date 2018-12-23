__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetCmdFree from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdFree(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdFree')
    # print(res)
    str1 = res["result"].split("\n")
    str2 = str1[1].split(" ")
    data = []
    for x in str2:
        if(x!=""):
            data.append(x)

    json_body = [
        {
            "measurement": "GetCmdFree",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "total": int(data[1]),
                "used": int(data[2]),
                "free": int(data[3]),
                "shared": int(data[4]),
                "buffers": int(data[5]),
                "cached": int(data[6]),
            }
        }
    ]

    influxDbClient.write_points(json_body)



if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetCmdFree(lepdClient, influxDbClient)
        time.sleep(1)

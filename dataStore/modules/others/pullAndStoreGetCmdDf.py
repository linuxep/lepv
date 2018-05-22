__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetCmdDf from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdDf(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdDf')
    # print(res)

    str1 = res["result"].split("\n")
    str2 = str1[3].split(' ')
    data = []
    for x in str2:
        if(x!=''):
            data.append(x)
    # for y in data:
    #     print(y)

    json_body = [
        {
            "measurement": "GetCmdDf",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "Filesystem": data[0],
                "Size": data[1],
                "Used": data[2],
                "Available": data[3],
                "Use%": data[4],
                "Mounted on": data[5]
            }
        }
    ]

    influxDbClient.write_points(json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetCmdDf(lepdClient, influxDbClient)
        time.sleep(1)

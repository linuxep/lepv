__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetCmdDmesg from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdDmesg(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdDmesg')
    # print(res)
    data = res["result"].split("\n")
    # for x in data:
    #     print(x)

    json_body = [
        {
            "measurement": "GetCmdDmesg",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "audit": data[7],
                "Adding":data[8],
                "NET": data[9],
                "e1000":data[12],
                "IPv6":data[13]

            }
        }
    ]

    influxDbClient.write_points(json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetCmdDmesg(lepdClient, influxDbClient)
        time.sleep(1)

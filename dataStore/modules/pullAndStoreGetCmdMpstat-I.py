__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetCmdMpstat-I from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdMpstat_I(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdMpstat-I')
    print(res)
    str1 = res["result"].split("\n")
    # for x in str1:
    #     print(x)
    data = []
    str2=str1[27].split(" ")
    for y in str2:
        if(y!=""):
            data.append(y)
    json_body = [
        {
            "measurement": "GetProcSwaps",

            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "CPU": float(data[1]),
                "HI/s": float(data[2]),
                "TIMER/s": float(data[3]),
                "NET_TX/s": float(data[4]),
                "NET_RX/s": float(data[5]),
                "BLOCK/s": float(data[6]),
                "IRQ_POLL/s": float(data[7]),
                "TASKLET/s": float(data[8]),
                "SCHED/s": float(data[9]),
                "HRTIMER/s": float(data[10]),
                "RCU/s": float(data[11])
            }
        }
    ]

    influxDbClient.write_points(json_body)



if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetCmdMpstat_I(lepdClient, influxDbClient)
        time.sleep(1)

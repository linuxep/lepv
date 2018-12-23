__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetCmdIostat from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdIostat(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdIostat')
    # print(res)
    mystr = res['result'].split('\n')
    # for x in mystr:
    #     print(x)
    # print(mystr[3])
    data = []
    mystr1 = mystr[3].split(' ')
    for y in mystr1:
        if(y!=''):
            data.append(y)
    # print(data)

    json_body = [
        {
            "measurement": "GetCmdIostat",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "Device": data[0],
                "rrqm/s": float(data[1]),
                "wrqm/s": float(data[2]),
                "r/s": float(data[3]),
                "w/s": float(data[4]),
                "rkB/s": float(data[5]),
                "wkB/s": float(data[6]),
                "avgrq-sz": float(data[7]),
                "avgqu-sz": float(data[8]),
                "await": float(data[9]),
                "r_await": float(data[10]),
                "w_await": float(data[11]),
                "svctm": float(data[12]),
                "%util": float(data[13])
            }
        }
    ]

    influxDbClient.write_points(json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(120):
        pullAndStoreGetCmdIostat(lepdClient, influxDbClient)
        time.sleep(1)

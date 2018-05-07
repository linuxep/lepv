__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetProcSwaps from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetProcSwaps(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetProcSwaps')
    print(res)
    mystr = res['result'].split('\n')
    x1 = mystr[1].split('\t')
    for x in x1 :
        print(x)



    json_body = [
        {
            "measurement": "GetProcSwaps",
            "tags": {

                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "FilenameType": x1[0],
                "Size": int(x1[1]),
                "Used": int(x1[2]),
                "Priority": int(x1[3])
            }
        }
    ]

    influxDbClient.write_points(json_body)

if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetProcSwaps(lepdClient, influxDbClient)
        time.sleep(1)

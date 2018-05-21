__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time
import re

'''
fetch data related to  GetCmdMpstat from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdMpstat(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdMpstat')
    # print(res)
    myStr = res['result'].split('\n')

    data = re.findall(r"\d+\.?\d*", myStr[10])


    json_body = [
        {
            "measurement": "GetCmdMpstat",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "%usr": float(data[0]),
                "%nice": float(data[1]),
                "%sys": float(data[2]),
                "%iowait": float(data[3]),
                "%irq": float(data[4]),
                "%soft": float(data[5]),
                "%steal": float(data[6]),
                "%guest": float(data[7]),
                "%gnice": float(data[8]),
                "%idle": float(data[9])
            }

        }
    ]

    influxDbClient.write_points(json_body)



if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(30):
        pullAndStoreGetCmdMpstat(lepdClient, influxDbClient)
        time.sleep(1)



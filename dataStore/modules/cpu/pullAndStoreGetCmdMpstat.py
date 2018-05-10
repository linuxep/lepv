__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetCmdMpstat from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdMpstat(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdMpstat')
    # print(res)
    myStr = res['result'].split('\n')

    x1 = myStr[10].split('    ')
    x2 = x1[10].split('   ')
    # for x in x1:
    #     print(x)
    # for z in x2:
    #     print(z)
    json_body = [
        {
            "measurement": "GetCmdMpstat",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "%usr": float(x1[2]),
                "%nice": float(x1[3]),
                "%sys": float(x1[4]),
                "%iowait": float(x1[5]),
                "%irq": float(x1[6]),
                "%soft": float(x1[7]),
                "%steal": float(x1[8]),
                "%guest": float(x1[9]),
                "%gnice": float(x2[0]),
                "%idle": float(x2[1])
            }

        }
    ]

    influxDbClient.write_points(json_body)



if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(60):
        pullAndStoreGetCmdMpstat(lepdClient, influxDbClient)
        time.sleep(1)



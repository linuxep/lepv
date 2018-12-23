__author__ = "李旭升 <programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."


from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time


'''
用lepdClient请求CPU相关数据并把返回的数据用influxDbClient存储到InfluxDB中
'''
def pullAndStoreGetProcCpuinfo(lepdClient,influxDbClient):
    res = lepdClient.sendRequest('GetProcCpuinfo')
    print(res)
    str1 = res["result"].split("\n")

    str=''
    for i in range(27):
        str=str+str1[i]
    # print(str)
    json_body = [
        {
            "measurement": "GetProcCpuinfo",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "cpuInfo":str
            }
        }
    ]

    influxDbClient.write_points(json_body)


if(__name__=='__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')

    pullAndStoreGetProcCpuinfo(lepdClient,influxDbClient)

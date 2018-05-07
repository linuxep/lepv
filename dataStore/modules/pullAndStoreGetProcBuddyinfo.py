__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetProcBuddyinfo from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetProcBuddyinfo(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetProcBuddyinfo')
    print(res)
    # str = res['result'].split('\n')
    # data = {}
    # for x in str:
    #
    #     x1 = x.replace('kB', '')
    #     x2 = x1.replace(' ', '')
    #     list = x2.split(':')
    #     if (len(list) == 2):
    #         data[list[0]] = list[1]
    #
    # # print(data)
    #
    # json_body = [
    #     {
    #         "measurement": "GetProcMeminfo",
    #         "tags": {
    #             # the address of lepd
    #             "server": lepdClient.server
    #         },
    #         # "time": "2017-03-12T22:00:00Z",
    #         "fields": {
    #             "MemTotal": data['MemTotal'],
    #             "MemFree": data['MemFree'],
    #             #   "MemAvailable": data['MemAvailable'],
    #             "Buffers": data['Buffers'],
    #             "Cached": data['Cached'],
    #             "SwapCached": data['MemTotal'],
    #             "Active": data['Active'],
    #             "Inactive": data['Inactive'],
    #             "Active(anon)": data['Active(anon)'],
    #             "Inactive(anon)": data['Inactive(anon)'],
    #             "Active(file)": data['Active(file)'],
    #             "Inactive(file)": data['Inactive(file)'],
    #             "Unevictable": data['Unevictable'],
    #             "Mlocked": data['Mlocked'],
    #             "SwapTotal": data['SwapTotal'],
    #             "SwapFree": data['SwapFree'],
    #             "Dirty": data['Dirty'],
    #             "Writeback": data['Writeback'],
    #             "AnonPages": data['AnonPages'],
    #             "Mapped": data['Mapped'],
    #             "Shmem": data['Shmem'],
    #             "Slab": data['Slab'],
    #             "SReclaimable": data['SReclaimable'],
    #             "SUnreclaim": data['SUnreclaim'],
    #             "KernelStack": data['KernelStack'],
    #             "PageTables": data['PageTables'],
    #             "NFS_Unstable": data['NFS_Unstable'],
    #             "Bounce": data['Bounce'],
    #             "WritebackTmp": data['WritebackTmp'],
    #             "CommitLimit": data['CommitLimit'],
    #             "Committed_AS": data['Committed_AS'],
    #             "VmallocTotal": data['VmallocTotal'],
    #             "VmallocUsed": data['VmallocUsed'],
    #             "VmallocChunk": data['VmallocChunk'],
    #             "HardwareCorrupted": data['HardwareCorrupted'],
    #             "AnonHugePages": data['AnonHugePages'],
    #             # "ShmemHugePages": data['ShmemHugePages'],
    #             # "ShmemPmdMapped": data['ShmemPmdMapped'],
    #             # "CmaTotal": data['CmaTotal'],
    #             # "CmaFree": data['CmaFree'],
    #             "HugePages_Total": data['HugePages_Total'],
    #             "HugePages_Free": data['HugePages_Free'],
    #             "HugePages_Rsvd": data['HugePages_Rsvd'],
    #             "HugePages_Surp": data['HugePages_Surp'],
    #             "Hugepagesize": data['Hugepagesize'],
    #             "DirectMap4k": data['DirectMap4k'],
    #             "DirectMap2M": data['DirectMap2M'],
    #             "DirectMap1G": data['DirectMap1G']
    #         }
    #     }
    # ]
    #
    # influxDbClient.write_points( json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetProcBuddyinfo(lepdClient, influxDbClient)
        time.sleep(1)

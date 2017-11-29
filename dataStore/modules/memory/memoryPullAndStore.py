__author__ = "李旭升 <programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import myInfluxDbClient

import time

'''
用lepdClient请求数据并把返回的数据用influxDbClient存储到InfluxDB中
'''
def pullAndStoreGetProcMeminfo(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetProcMeminfo')
    print(res)
    str = res['result'].split('\n')
    data = {}
    for x in str:

        x1 = x.replace('kB', '')
        x2 = x1.replace(' ', '')
        list = x2.split(':')
        if (len(list) == 2):
            data[list[0]] = list[1]

    # print(data)

    json_body = [
        {
            "measurement": "GetProcMeminfo",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "MemTotal": data['MemTotal'],
                "MemFree": data['MemFree'],
                #   "MemAvailable": data['MemAvailable'],
                "Buffers": data['Buffers'],
                "Cached": data['Cached'],
                "SwapCached": data['MemTotal'],
                "Active": data['Active'],
                "Inactive": data['Inactive'],
                "Active(anon)": data['Active(anon)'],
                "Inactive(anon)": data['Inactive(anon)'],
                "Active(file)": data['Active(file)'],
                "Inactive(file)": data['Inactive(file)'],
                "Unevictable": data['Unevictable'],
                "Mlocked": data['Mlocked'],
                "SwapTotal": data['SwapTotal'],
                "SwapFree": data['SwapFree'],
                "Dirty": data['Dirty'],
                "Writeback": data['Writeback'],
                "AnonPages": data['AnonPages'],
                "Mapped": data['Mapped'],
                "Shmem": data['Shmem'],
                "Slab": data['Slab'],
                "SReclaimable": data['SReclaimable'],
                "SUnreclaim": data['SUnreclaim'],
                "KernelStack": data['KernelStack'],
                "PageTables": data['PageTables'],
                "NFS_Unstable": data['NFS_Unstable'],
                "Bounce": data['Bounce'],
                "WritebackTmp": data['WritebackTmp'],
                "CommitLimit": data['CommitLimit'],
                "Committed_AS": data['Committed_AS'],
                "VmallocTotal": data['VmallocTotal'],
                "VmallocUsed": data['VmallocUsed'],
                "VmallocChunk": data['VmallocChunk'],
                "HardwareCorrupted": data['HardwareCorrupted'],
                "AnonHugePages": data['AnonHugePages'],
                # "ShmemHugePages": data['ShmemHugePages'],
                # "ShmemPmdMapped": data['ShmemPmdMapped'],
                # "CmaTotal": data['CmaTotal'],
                # "CmaFree": data['CmaFree'],
                "HugePages_Total": data['HugePages_Total'],
                "HugePages_Free": data['HugePages_Free'],
                "HugePages_Rsvd": data['HugePages_Rsvd'],
                "HugePages_Surp": data['HugePages_Surp'],
                "Hugepagesize": data['Hugepagesize'],
                "DirectMap4k": data['DirectMap4k'],
                "DirectMap2M": data['DirectMap2M'],
                "DirectMap1G": data['DirectMap1G']
            }
        }
    ]

    influxDbClient.write_points('www.rmlink.cn', json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('www.rmlink.cn')
    influxDbClient = myInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetProcMeminfo(lepdClient, influxDbClient)
        time.sleep(1)

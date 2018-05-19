__author__ = "李旭升 programmerli@foxmail.com > "

__copyright__ = "Licensed under GPLv2 or later."


'''
用lepdClient请求数据并把返回的数据用influxDbClient存储到InfluxDB中
'''

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

def pullAndStoreGetProcMeminfo(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetProcMeminfo')
    # print(res)
    mystr = res['result'].split('\n')
    data = {}
    for x in mystr:

        x1 = x.replace('kB', '')
        x2 = x1.replace(' ', '')
        list = x2.split(':')
        if (len(list) == 2):
            data[list[0]] = list[1]


    #print(data['Active'])


    json_body = [
        {
            "measurement": "GetProcMeminfo",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "MemTotal": int(data['MemTotal']),
                "MemFree": int(data['MemFree']),
                #   "MemAvailable": data['MemAvailable'],
                "Buffers": int(data['Buffers']),
                "Cached": int(data['Cached']),
                "SwapCached": int(data['MemTotal']),
                "Active": int(data['Active']),
                "Inactive": int(data['Inactive']),
                "Active(anon)": int(data['Active(anon)']),
                "Inactive(anon)": int(data['Inactive(anon)']),
                "Active(file)": int(data['Active(file)']),
                "Inactive(file)": int(data['Inactive(file)']),
                "Unevictable": int(data['Unevictable']),
                "Mlocked": int(data['Mlocked']),
                "SwapTotal": int(data['SwapTotal']),
                "SwapFree": int(data['SwapFree']),
                "Dirty": int(data['Dirty']),
                "Writeback": int(data['Writeback']),
                "AnonPages": int(data['AnonPages']),
                "Mapped": int(data['Mapped']),
                "Shmem": int(data['Shmem']),
                "Slab": int(data['Slab']),
                "SReclaimable": int(data['SReclaimable']),
                "SUnreclaim": int(data['SUnreclaim']),
                "KernelStack": int(data['KernelStack']),
                "PageTables": int(data['PageTables']),
                "NFS_Unstable": int(data['NFS_Unstable']),
                "Bounce": int(data['Bounce']),
                "WritebackTmp": int(data['WritebackTmp']),
                "CommitLimit": int(data['CommitLimit']),
                "Committed_AS": int(data['Committed_AS']),
                "VmallocTotal": int(data['VmallocTotal']),
                "VmallocUsed": int(data['VmallocUsed']),
                "VmallocChunk": int(data['VmallocChunk']),
                "HardwareCorrupted": int(data['HardwareCorrupted']),
                "AnonHugePages": int(data['AnonHugePages']),
                # "ShmemHugePages": data['ShmemHugePages'],
                # "ShmemPmdMapped": data['ShmemPmdMapped'],
                # "CmaTotal": data['CmaTotal'],
                # "CmaFree": data['CmaFree'],
                "HugePages_Total": int(data['HugePages_Total']),
                "HugePages_Free": int(data['HugePages_Free']),
                "HugePages_Rsvd": int(data['HugePages_Rsvd']),
                "HugePages_Surp": int(data['HugePages_Surp']),
                "Hugepagesize": int(data['Hugepagesize']),
                "DirectMap4k": int(data['DirectMap4k']),
                "DirectMap2M": int(data['DirectMap2M']),
                "DirectMap1G": int(data['DirectMap1G'])
            }
        }
    ]

    influxDbClient.write_points( json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(10):
        pullAndStoreGetProcMeminfo(lepdClient, influxDbClient)
        time.sleep(1)

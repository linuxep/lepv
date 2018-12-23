__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient


import time

'''
fetch data related to  GetProcZoneinfo from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetProcZoneinfo(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetProcZoneinfo')
    print(res)
    data = {}

    mystr = res['result'].split('\n')
    for x in mystr:
        x1 = x.strip()
        x2 = x1.split(' ')
        #把所有参数没有存完
        if (len(x2) == 2):
            data[x2[0]]=x2[1]




    json_body = [
        {
            "measurement": "GetProcZoneinfo",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",
            "fields": {
                "nr_inactive_anon": int(data['nr_inactive_anon']),
                "nr_active_anon": int(data['nr_active_anon']),
                "nr_inactive_file": int(data['nr_inactive_file']),
                "nr_active_file": int(data['nr_active_file']),
                "nr_unevictable": int(data['nr_unevictable']),
                "nr_slab_reclaimable": int(data['nr_slab_reclaimable']),
                "nr_slab_unreclaimable": int(data['nr_slab_unreclaimable']),
                "nr_isolated_anon": int(data['nr_isolated_anon']),
                "nr_isolated_file": int(data['nr_isolated_file']),
                "workingset_refault": int(data['workingset_refault']),
                "workingset_activate": int(data['workingset_activate']),
                "workingset_nodereclaim": int(data['workingset_nodereclaim']),
                "nr_anon_pages": int(data['nr_anon_pages']),
                "nr_file_pages": int(data['nr_file_pages']),
                "nr_writeback": int(data['nr_writeback']),
                "nr_writeback_temp": int(data['nr_writeback_temp']),
                "nr_shmem_hugepages": int(data['nr_shmem_hugepages']),
                "nr_shmem_pmdmapped": int(data['nr_shmem_pmdmapped']),
                "nr_anon_transparent_hugepages": int(data['nr_anon_transparent_hugepages']),
                "nr_vmscan_write": int(data['nr_vmscan_write']),
                "nr_vmscan_immediate_reclaim": int(data['nr_vmscan_immediate_reclaim']),
                "nr_free_pages": int(data['nr_free_pages']),
                "nr_zone_inactive_anon": int(data['nr_zone_inactive_anon']),
                "nr_zone_active_anon": int(data['nr_zone_active_anon']),
                "nr_zone_inactive_file": int(data['nr_zone_inactive_file']),
                "nr_zone_active_file": int(data['nr_zone_active_file']),
                "nr_zone_unevictable": int(data['nr_zone_unevictable']),
                "nr_zone_write_pending": int(data['nr_zone_write_pending']),
                "nr_page_table_pages": int(data['nr_page_table_pages']),
                "nr_kernel_stack": int(data['nr_kernel_stack']),
                "numa_foreign": int(data['numa_foreign']),
                "numa_interleave": int(data['numa_interleave'])
            }
        }
    ]

    influxDbClient.write_points(json_body)

if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetProcZoneinfo(lepdClient, influxDbClient)
        time.sleep(1)

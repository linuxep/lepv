__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient



import time

'''
fetch data related to  GetProcVmstat from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetProcVmstat(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetProcVmstat')
    # print(res)
    str = res['result'].split('\n')
    data = {}
    for x in str:
        list = x.split(' ')
        if (len(list) == 2):
            data[list[0]] = list[1]

    print(data)

    # json_body = [
    #     {
    #         "measurement": "GetProcVmstat",
    #         "tags": {
    #             # the address of lepd
    #             "server": lepdClient.server
    #         },
    #         # "time": "2017-03-12T22:00:00Z",
    #         "fields": {
    #             "compact_stall": data['MemTotal'],
    #             "balloon_migrate": data['MemFree'],
    #             "nr_unevictable": data['Buffers'],
    #             "nr_vmscan_write": data['Cached'],
    #             "pgskip_movable": data['MemTotal'],
    #             "thp_fault_fallback": data['Active'],
    #             "nr_anon_pages": data['Inactive'],
    #             "numa_other": data['Active(anon)'],
    #             "thp_split_page": data['Inactive(anon)'],
    #             "unevictable_pgs_stranded": data['Active(file)'],
    #             "nr_shmem_pmdmapped": data['Inactive(file)'],
    #             "nr_shmem": data['Unevictable'],
    #             "nr_zone_write_pending": data['Mlocked'],
    #             "compact_migrate_scanned": data['SwapTotal'],
    #             "nr_zone_active_anon": data['SwapFree'],
    #             "pglazyfree": data['Dirty'],
    #             "numa_foreign": data['Writeback'],
    #             "pglazyfreed": data['AnonPages'],
    #             "nr_zone_active_file": data['Mapped'],
    #             "numa_pte_updates": data['Shmem'],
    #             "pgscan_direct_throttle": data['Slab'],
    #             "kswapd_low_wmark_hit_quickly": data['SReclaimable'],
    #             "nr_dirtied": data['SUnreclaim'],
    #             "htlb_buddy_alloc_fail": data['KernelStack'],
    #             "nr_dirty_background_threshold": data['PageTables'],
    #             "pgalloc_dma32": data['NFS_Unstable'],
    #             "compact_daemon_migrate_scanned": data['Bounce'],
    #             "unevictable_pgs_culled": data['WritebackTmp'],
    #             "numa_miss": data['Mapped'],
    #             "compact_isolated": data['Shmem'],
    #             "pswpout": data['Slab'],
    #             "pgsteal_kswapd": data['SReclaimable'],
    #             "thp_split_pud": data['SUnreclaim'],
    #             "unevictable_pgs_mlocked": data['KernelStack'],
    #             "thp_zero_page_alloc": data['PageTables'],
    #             "workingset_activate": data['NFS_Unstable'],
    #             "unevictable_pgs_cleared": data['Bounce'],
    #             "pgalloc_movable": data['WritebackTmp'],
    #             "pageoutrun": data['Mapped'],
    #             "pgfault": data['Shmem'],
    #             "nr_unstable": data['Slab'],
    #             "kswapd_high_wmark_hit_quickly": data['SReclaimable'],
    #             "thp_deferred_split_page": data['SUnreclaim'],
    #             "thp_file_mapped": data['KernelStack'],
    #             "pgscan_kswapd": data['PageTables'],
    #             "nr_writeback_temp": data['NFS_Unstable'],
    #             "nr_dirty_threshold": data['Bounce'],
    #             "nr_mlock": data['WritebackTmp'],
    #             "htlb_buddy_alloc_success": data['Mapped'],
    #             "nr_isolated_anon": data['Shmem'],
    #             "allocstall_normal": data['Slab'],
    #             "nr_mapped": data['SReclaimable'],
    #             "numa_local": data['SUnreclaim'],
    #             "nr_zone_inactive_anon": data['KernelStack'],
    #             "pgmajfault": data['PageTables'],
    #             "thp_fault_alloc": data['NFS_Unstable'],
    #             "compact_success": data['Bounce'],
    #             "allocstall_dma": data['WritebackTmp'],
    #             "thp_split_pmd": data['Mapped'],
    #             "nr_bounce": data['Shmem'],
    #             "thp_zero_page_alloc_failed": data['Slab'],
    #             "pgdeactivate": data['SReclaimable'],
    #             "allocstall_dma32": data['SUnreclaim'],
    #             "nr_file_pages": data['KernelStack'],
    #             "nr_anon_transparent_hugepages": data['PageTables'],
    #             "compact_fail": data['NFS_Unstable'],
    #             "nr_page_table_pages": data['Bounce'],
    #             "numa_hint_faults": data['WritebackTmp'],
    #             "pgskip_dma32": data['Mapped'],
    #             "numa_pages_migrated": data['Shmem'],
    #             "nr_vmscan_immediate_reclaim": data['Slab'],
    #             "nr_zone_unevictable": data['SReclaimable'],
    #             "pgmigrate_fail": data['SUnreclaim'],
    #             "compact_daemon_wake": data['KernelStack'],
    #             "pgskip_dma": data['PageTables'],
    #             "nr_active_anon": data['NFS_Unstable'],
    #             "pgpgout": data['Bounce'],
    #             "pgskip_normal": data['WritebackTmp'],
    #             "pginodesteal": data['NFS_Unstable'],
    #             "nr_zspages": data['Bounce'],
    #             "unevictable_pgs_rescued": data['WritebackTmp'],
    #             "pgalloc_dma": data['Mapped'],
    #             "pswpin": data['Shmem'],
    #             "thp_collapse_alloc": data['Slab'],
    #             "nr_writeback": data['SReclaimable'],
    #             "nr_free_pages": data['SUnreclaim'],
    #             "pgpgin": data['KernelStack'],
    #             "pgalloc_normal": data['PageTables'],
    #             "slabs_scanned": data['NFS_Unstable'],
    #             "thp_file_alloc": data['Bounce'],
    #             "nr_written": data['WritebackTmp'],
    #             "compact_free_scanned": data['NFS_Unstable'],
    #             "numa_hint_faults_local": data['Bounce'],
    #             "drop_pagecache": data['WritebackTmp'],
    #             "thp_split_page_failed": data['Mapped'],
    #             "nr_zone_inactive_file": data['Shmem'],
    #             "unevictable_pgs_munlocked": data['Slab'],
    #             "nr_slab_reclaimable": data['SReclaimable'],
    #             "allocstall_movable": data['SUnreclaim'],
    #             "oom_kill": data['KernelStack'],
    #             "nr_free_cma": data['PageTables'],
    #             "balloon_inflate": data['NFS_Unstable'],
    #             "numa_huge_pte_updates": data['Bounce'],
    #             "unevictable_pgs_scanned": data['WritebackTmp'], "": data['PageTables'],
    #             "nr_active_file": data['NFS_Unstable'],
    #             "nr_shmem_hugepages": data['Bounce'],
    #             "kswapd_inodesteal": data['WritebackTmp'],
    #             "pgscan_direct": data['Mapped'],
    #             "numa_interleave": data['Shmem'],
    #             "nr_slab_unreclaimable": data['Slab'],
    #             "thp_collapse_alloc_failed": data['SReclaimable'],
    #             "workingset_refault": data['SUnreclaim'],
    #             "compact_daemon_free_scanned": data['KernelStack'],
    #             "zone_reclaim_failed": data['PageTables'],
    #             "nr_isolated_file": data['NFS_Unstable'],
    #             "nr_inactive_anon": data['Bounce'],
    #             "pgrotated": data['WritebackTmp'], "": data['PageTables'],
    #             "nr_kernel_stack": data['NFS_Unstable'],
    #             "numa_hit": data['Bounce'],
    #             "nr_dirty": data['WritebackTmp'],
    #             "workingset_nodereclaim": data['Mapped'],
    #             "drop_slab": data['Shmem'],
    #             "nr_inactive_file": data['Slab'],
    #             "pgrefill": data['SReclaimable'],
    #             "pgmigrate_success": data['SUnreclaim'],
    #             "pgactivate": data['KernelStack'],
    #             "balloon_deflate": data['PageTables'],
    #             "pgfree": data['NFS_Unstable'],
    #             "pgsteal_direct": data['Bounce']
    #         }
    #     }
    # ]
    #
    # influxDbClient.write_points('www.rmlink.cn', json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetProcVmstat(lepdClient, influxDbClient)
        time.sleep(1)

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

    json_body = [
        {
            "measurement": "GetProcVmstat",
            "tags": {
                # the address of lepd
                "server": lepdClient.server
            },
            # "time": "2017-03-12T22:00:00Z",


            "fields": {
                "compact_stall" : int(data['compact_stall']),
                "balloon_migrate": int(data['balloon_migrate']),
                "nr_unevictable": int(data['nr_unevictable']),
                "nr_vmscan_write": int(data['nr_vmscan_write']),
                "pgskip_movable": int(data['pgskip_movable']),
                "thp_fault_fallback": int(data['thp_fault_fallback']),
                "nr_anon_pages": int(data['nr_anon_pages']),
                "numa_other": int(data['numa_other']),
                "thp_split_page": int(data['thp_split_page']),
                "unevictable_pgs_stranded": int(data['unevictable_pgs_stranded']),
                "nr_shmem_pmdmapped": int(data['nr_shmem_pmdmapped']),
                "nr_shmem": int(data['nr_shmem']),
                "nr_zone_write_pending": int(data['nr_zone_write_pending']),
                "compact_migrate_scanned": int(data['compact_migrate_scanned']),
                "nr_zone_active_anon": int(data['nr_zone_active_anon']),
                "pglazyfree": int(data['pglazyfree']),
                "numa_foreign": int(data['numa_foreign']),
                "pglazyfreed": int(data['pglazyfreed']),
                "nr_zone_active_file": int(data['nr_zone_active_file']),
                "numa_pte_updates": int(data['numa_pte_updates']),
                "pgscan_direct_throttle":int(data['pgscan_direct_throttle']),
                "kswapd_low_wmark_hit_quickly": int(data['kswapd_low_wmark_hit_quickly']),
                "nr_dirtied": int(data['nr_dirtied']),
                "htlb_buddy_alloc_fail": int(data['htlb_buddy_alloc_fail']),
                "nr_dirty_background_threshold": int(data['nr_dirty_background_threshold']),
                "pgalloc_dma32": int(data['pgalloc_dma32']),
                "compact_daemon_migrate_scanned": int(data['compact_daemon_migrate_scanned']),
                "unevictable_pgs_culled": int(data['unevictable_pgs_culled']),
                "numa_miss": int(data['numa_miss']),
                "compact_isolated": int(data['compact_isolated']),
                "pswpout": int(data['pswpout']),
                "pgsteal_kswapd": int(data['pgsteal_kswapd']),
                "thp_split_pud": int(data['thp_split_pud']),
                "unevictable_pgs_mlocked": int(data['unevictable_pgs_mlocked']),
                "thp_zero_page_alloc": int(data['thp_zero_page_alloc']),
                "workingset_activate": int(data['workingset_activate']),
                "unevictable_pgs_cleared": int(data['unevictable_pgs_cleared']),
                "pgalloc_movable": int(data['pgalloc_movable']),
                "pageoutrun": int(data['pageoutrun']),
                "pgfault": int(data['pgfault']),
                "nr_unstable": int(data['nr_unstable']),
                "kswapd_high_wmark_hit_quickly": int(data['kswapd_high_wmark_hit_quickly']),
                "thp_deferred_split_page": int(data['thp_deferred_split_page']),
                "thp_file_mapped": int(data['thp_file_mapped']),
                "pgscan_kswapd": int(data['pgscan_kswapd']),
                "nr_writeback_temp": int(data['nr_writeback_temp']),
                "nr_dirty_threshold": int(data['nr_dirty_threshold']),
                "nr_mlock": int(data['nr_mlock']),
                "htlb_buddy_alloc_success": int(data['htlb_buddy_alloc_success']),
                "nr_isolated_anon": int(data['nr_isolated_anon']),
                "allocstall_normal": int(data['allocstall_normal']),
                "nr_mapped": int(data['nr_mapped']),
                "numa_local": int(data['numa_local']),
                "nr_zone_inactive_anon": int(data['nr_zone_inactive_anon']),
                "pgmajfault": int(data['pgmajfault']),
                "thp_fault_alloc": int(data['thp_fault_alloc']),
                "compact_success": int(data['compact_success']),
                "allocstall_dma": int(data['allocstall_dma']),
                "thp_split_pmd": int(data['thp_split_pmd']),
                "nr_bounce": int(data['nr_bounce']),
                "thp_zero_page_alloc_failed": int(data['thp_zero_page_alloc_failed']),
                "pgdeactivate": int(data['pgdeactivate']),
                "allocstall_dma32": int(data['allocstall_dma32']),
                "nr_file_pages": int(data['nr_file_pages']),
                "nr_anon_transparent_hugepages": int(data['nr_anon_transparent_hugepages']),
                "compact_fail": int(data['compact_fail']),
                "nr_page_table_pages": int(data['nr_page_table_pages']),
                "numa_hint_faults": int(data['numa_hint_faults']),
                "pgskip_dma32": int(data['pgskip_dma32']),
                "numa_pages_migrated": int(data['numa_pages_migrated']),
                "nr_vmscan_immediate_reclaim": int(data['nr_vmscan_immediate_reclaim']),
                "nr_zone_unevictable": int(data['nr_zone_unevictable']),
                "pgmigrate_fail": int(data['pgmigrate_fail']),
                "compact_daemon_wake": int(data['compact_daemon_wake']),
                "pgskip_dma": int(data['pgskip_dma']),
                "nr_active_anon": int(data['nr_active_anon']),
                "pgpgout": int(data['pgpgout']),
                "pgskip_normal": int(data['pgskip_normal']),
                "pginodesteal": int(data['pginodesteal']),
                "nr_zspages": int(data['nr_zspages']),
                "unevictable_pgs_rescued": int(data['unevictable_pgs_rescued']),
                "pgalloc_dma": int(data['pgalloc_dma']),
                "pswpin": int(data['pswpin']),
                "thp_collapse_alloc": int(data['thp_collapse_alloc']),
                "nr_writeback": int(data['nr_writeback']),
                "nr_free_pages": int(data['nr_free_pages']),
                "pgpgin": int(data['pgpgin']),
                "pgalloc_normal": int(data['pgalloc_normal']),
                "slabs_scanned": int(data['slabs_scanned']),
                "thp_file_alloc": int(data['thp_file_alloc']),
                "nr_written": int(data['nr_written']),
                "compact_free_scanned": int(data['compact_free_scanned']),
                "numa_hint_faults_local": int(data['numa_hint_faults_local']),
                "drop_pagecache": int(data['drop_pagecache']),
                "thp_split_page_failed": int(data['thp_split_page_failed']),
                "nr_zone_inactive_file": int(data['nr_zone_inactive_file']),
                "unevictable_pgs_munlocked": int(data['unevictable_pgs_munlocked']),
                "nr_slab_reclaimable": int(data['nr_slab_reclaimable']),
                "allocstall_movable": int(data['allocstall_movable']),
                "oom_kill": int(data['oom_kill']),
                "nr_free_cma": int(data['nr_free_cma']),
                "balloon_inflate": int(data['balloon_inflate']),
                "numa_huge_pte_updates": int(data['numa_huge_pte_updates']),
                "unevictable_pgs_scanned": int(data['unevictable_pgs_scanned']),
                "nr_active_file": int(data['nr_active_file']),
                "nr_shmem_hugepages": int(data['nr_shmem_hugepages']),
                "kswapd_inodesteal": int(data['kswapd_inodesteal']),
                "pgscan_direct": int(data['pgscan_direct']),
                "numa_interleave": int(data['numa_interleave']),
                "nr_slab_unreclaimable": int(data['nr_slab_unreclaimable']),
                "thp_collapse_alloc_failed": int(data['thp_collapse_alloc_failed']),
                "workingset_refault": int(data['workingset_refault']),
                "compact_daemon_free_scanned": int(data['compact_daemon_free_scanned']),
                "zone_reclaim_failed": int(data['zone_reclaim_failed']),
                "nr_isolated_file": int(data['nr_isolated_file']),
                "nr_inactive_anon": int(data['nr_inactive_anon']),
                "pgrotated": int(data['pgrotated']),
                "nr_kernel_stack": int(data['nr_kernel_stack']),
                "numa_hit": int(data['numa_hit']),
                "nr_dirty": int(data['nr_dirty']),
                "workingset_nodereclaim": int(data['workingset_nodereclaim']),
                "drop_slab": int(data['drop_slab']),
                "nr_inactive_file": int(data['nr_inactive_file']),
                "pgrefill": int(data['pgrefill']),
                "pgmigrate_success": int(data['pgmigrate_success']),
                "pgactivate": int(data['pgactivate']),
                "balloon_deflate": int(data['balloon_deflate']),
                "pgfree": int(data['pgfree']),
                "pgsteal_direct": int(data['pgsteal_direct'])
            }
        }
    ]

    influxDbClient.write_points(json_body)


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetProcVmstat(lepdClient, influxDbClient)
        time.sleep(1)

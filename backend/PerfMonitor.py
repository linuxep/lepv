"""Module for Perf related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from backend.LepDClient import LepDClient
import pprint

__author__ = 'xmac'

class PerfMonitor:

    def __init__(self, server):
        self.server = server
        self.client = LepDClient(self.server)

    def getPerfCpuClock(self):
        return self.client.getCmdPerfCpuclock()

if( __name__ =='__main__' ):
    monitor = PerfMonitor('www.linuxxueyuan.com')

    pp = pprint.PrettyPrinter(indent=2)
    
    while(1):
        result = monitor.getPerfCpuClock()['result']
        print(len(result))
    # pp.pprint(monitor.getPerfCpuClock())


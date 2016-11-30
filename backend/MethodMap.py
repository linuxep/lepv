"""Module for easier review of mathod mapping, from URL down to LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import pprint

class MethodMap:

    def __init__(self):
        pass
        
    def getMap(self):
        methodMap = []

        methodMapItem = {}
        methodMapItem['url'] = '/status/cpu'
        methodMapItem['viewMethod'] = 'getComponentStatus'
        methodMapItem['moduleMethod'] = 'CPUMonitor.getStatus'
        methodMapItem['lepdMethod'] = 'GetCmdMpstat'
        methodMap.append(methodMapItem)

        methodMapItem = {}
        methodMapItem['url'] = '/status/memory'
        methodMapItem['viewMethod'] = 'getComponentStatus'
        methodMapItem['moduleMethod'] = 'MemoryMonitor.getStatus'
        methodMapItem['lepdMethod'] = 'GetProcMeminfo'
        methodMap.append(methodMapItem)

        methodMapItem = {}
        methodMapItem['url'] = '/status/io'
        methodMapItem['viewMethod'] = 'getComponentStatus'
        methodMapItem['moduleMethod'] = 'IOMonitor.getStatus'
        methodMapItem['lepdMethod'] = 'GetCmdIostat'
        methodMap.append(methodMapItem)

        methodMapItem = {}
        methodMapItem['url'] = '/status/avgload'
        methodMapItem['viewMethod'] = 'getComponentStatus'
        methodMapItem['moduleMethod'] = 'CPUMonitor.getAverageLoad'
        methodMapItem['lepdMethod'] = 'GetProcLoadavg'
        methodMap.append(methodMapItem)

        methodMapItem = {}
        methodMapItem['url'] = '/cpustat'
        methodMapItem['viewMethod'] = 'getCpuStat'
        methodMapItem['moduleMethod'] = 'CPUMonitor.getStat'
        methodMapItem['lepdMethod'] = 'GetCmdMpstat'
        methodMap.append(methodMapItem)

        methodMapItem = {}
        methodMapItem['url'] = '/cputop'
        methodMapItem['viewMethod'] = 'getCpuTopData'
        methodMapItem['moduleMethod'] = 'CPUMonitor.getTopOutput'
        methodMapItem['lepdMethod'] = 'GetCmdTop'
        methodMap.append(methodMapItem)

        methodMapItem = {}
        methodMapItem['url'] = '/perfcpu'
        methodMapItem['viewMethod'] = 'getPerfCpuClockData'
        methodMapItem['moduleMethod'] = 'PerfMonitor.getPerfCpuClock'
        methodMapItem['lepdMethod'] = 'GetCmdPerfCpuclock'
        methodMap.append(methodMapItem)

        # methodMapItem = {}
        # methodMapItem['url'] = '/memstat'
        # methodMapItem['viewMethod'] = 'getMemoryStat'
        # methodMapItem['moduleMethod'] = 'MemoryMonitor.getMemoryStat'
        # methodMapItem['lepdMethod'] = 'GetCmdSmem'
        # methodMap.append(methodMapItem)

        methodMapItem = {}
        methodMapItem['url'] = '/ping'
        methodMapItem['viewMethod'] = 'pingServer'
        methodMapItem['moduleMethod'] = 'LepDClient.ping'
        methodMapItem['lepdMethod'] = 'SayHello'
        methodMap.append(methodMapItem)

        methodMapItem = {}
        methodMapItem['url'] = '/capacity/cpu'
        methodMapItem['viewMethod'] = 'getComponentCapacity'
        methodMapItem['moduleMethod'] = 'CPUMonitor.getCapacity'
        methodMapItem['lepdMethod'] = 'GetProcCpuinfo'
        methodMap.append(methodMapItem)

        methodMapItem = {}
        methodMapItem['url'] = '/capacity/memory'
        methodMapItem['viewMethod'] = 'getComponentCapacity'
        methodMapItem['moduleMethod'] = 'MemoryMonitor.getCapacity'
        methodMapItem['lepdMethod'] = 'GetProcMeminfo'
        methodMap.append(methodMapItem)

        methodMapItem = {}
        methodMapItem['url'] = '/capacity/io'
        methodMapItem['viewMethod'] = 'getComponentCapacity'
        methodMapItem['moduleMethod'] = 'IOMonitor.getCapacity'
        methodMapItem['lepdMethod'] = 'GetCmdDf'
        methodMap.append(methodMapItem)
        
        return methodMap


if( __name__ =='__main__' ):

    pp = pprint.PrettyPrinter(indent=2)
    
    methods = MethodMap()
    pp.pprint(methods.getMap())






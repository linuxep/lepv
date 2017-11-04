#encoding: utf-8
"""Module for internationalization"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

class Languages:

    def __init__(self):
        pass
        
    def getLanguagePackForCN(self):
        pack = {}

        pack["Summary"] = '概况'
        pack['CPU'] = '处理器'
        pack['Memory'] = '内存'
        pack['IO'] = '磁盘'
        pack['Perf'] = 'Perf'
        
        pack['SystemSummary'] = '系统概况'
        pack['TotalDiskSpace'] = '磁盘总空间'
        pack['FreeDiskSpace'] = '空闲磁盘空间'
        pack['Settings'] = '设置'
        pack['Server'] = '服务器'
        pack['Port'] = '端口'
        pack['Connect'] = '连接'
        pack['Configurations'] = '配置'
        pack['Language'] = '语言'

        pack['perfTableTitle'] = '基于Symbol的时间分布'
        pack['perfTableTitleFull'] = '基于Symbol的时间分布 (perf top)'
        
        pack['ioChartTitle'] = 'I/O吞吐量'
        pack['ioTopTableTitle'] = 'I/O TOP'
        
        pack['memoryConsumptionChartTitle'] = '内存消耗（单位: MB)'
        pack['ramChartTitle'] = '消耗的内存、Page Cahe(Buffers, Cached)和空闲的内存'
        pack['memoryPssDonutChartTitle'] = '应用程序内存消耗比例分布(基于PSS)'
        pack['memoryPssAgainstTotalChartTitle'] = '应用程序耗费内存占总内存比例'

        pack['averageLoadChartTitle'] = 'Average Load'
        pack['averageLoadChartTitleFull'] = 'Average Load: CPU的平均负载; 当达到0.7*核数时，负载较重; 当达到1.0*核数时，CPU是性能瓶颈'
        
        pack['cpuUserGroupChartTitle'] = 'CPU Stat: User+Sys+Nice'
        pack['cpuUserGroupChartTitleFull'] = 'CPU Stat: User+Sys+Nice; 进程上下文占据的时间比例，如果是多核，可由此观察CPU的负载均衡'
        
        pack['cpuIdleGroupChartTitle'] = 'CPU Stat: Idle'
        pack['cpuIdleGroupChartTitleFull'] = 'CPU Stat: Idle; 系统空闲占据的时间比例，如果是多核，可由此观察CPU的负载均衡'
        
        pack['cpuIrqGroupChartTitle'] = 'CPU Stat: IRQ + SoftIRQ'
        pack['cpuIrqGroupChartTitleFull'] = 'CPU Stat: IRQ + SoftIRQ; 中断/软中断占据的时间比例，如果是多核，可由此观察中断/软中断的负载均衡'
        
        pack['cpuStatRatioChartTitle'] = 'CPU Stat'
        pack['cpuStatRatioChartTitleFull'] = 'CPU Stat; 各种上下文占据的时间'
        
        return pack
    
    def getLanguagePackForEN(self):
        pack = {}
        pack["Summary"] = 'Summary'
        pack['CPU'] = 'CPU'
        
        return pack

if( __name__ =='__main__' ):
    client = Languages()
    client.getLanguagePack()






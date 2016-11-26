"""Module for I/O related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from backend.LepDClient import LepDClient
import re
import datetime
import pprint
from decimal import Decimal

class IOMonitor:

    def __init__(self, server, config='release'):
        self.server = server
        self.client = LepDClient(self.server)
        self.config = config

    def getStatus(self):

        startTime = datetime.datetime.now()
        
        result = self.client.getIostatResult()
        
        endTime = datetime.datetime.now()
        
        rawResult = result[:]
        
        headerLine = result.pop(0)

        duration = "%.1f" % ((endTime - startTime).total_seconds())
        ioStatus = {}
        ioStatus['lepdDuration'] = duration
        ioStatus['disks'] = {}
        ioStatus['diskCount'] = 0
        ioStatus['ratio'] = 0
        for line in result:
            if (line.strip() == ""):
                continue

            lineValues = line.split()

            deviceName = lineValues[0]
            ioStatus['diskCount'] += 1
            ioStatus['disks'][deviceName] = {}

            ioStatus['disks'][deviceName]['rkbs'] = lineValues[5]
            ioStatus['disks'][deviceName]['wkbs'] = lineValues[6]
            ioStatus['disks'][deviceName]['ratio'] = lineValues[-1]
            
            thisDiskRatio = Decimal(lineValues[-1])
            if (thisDiskRatio > ioStatus['ratio']):
                ioStatus['ratio'] = thisDiskRatio

        endTime2 = datetime.datetime.now()
        duration = "%.1f" % ((endTime2 - endTime).total_seconds())
        ioStatus['lepvParsingDuration'] = duration
        
        responseData = {}
        responseData['data'] = ioStatus
        responseData['rawResult'] = rawResult
        return responseData
    
    def getCapacity(self):
        diskInfo = self.client.getCmdDf()

        capacity = {}
        capacity['diskTotal'] = diskInfo['size']
        capacity['diskUsed'] = diskInfo['used']
        
        return capacity


    # Total DISK READ :    1025.66 M/s | Total DISK WRITE :       0.00 B/s
    # Actual DISK READ:     808.10 M/s | Actual DISK WRITE:       0.00 B/s
    # TID  PRIO  USER     DISK READ  DISK WRITE  SWAPIN      IO    COMMAND
    # 26014 be/4 root      323.24 M/s    0.00 B/s  0.00 %  8.96 % dd if=/dev/sda of=/dev/null
    # 26035 be/4 root      702.42 M/s    0.00 B/s  0.00 %  0.47 % dd if=/dev/sda of=/dev/null
    # 1 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % init
    # 2 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % [kthreadd]
    # 3 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % [ksoftirqd/0]
    # 5 be/0 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % [kworker/0:0H]
    # 7 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % [rcu_sched]
    # 8 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % [rcu_bh]
    # 9 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % [rcuos/0]
    # 10 be/4 root        0.00 B/s    0.00 B/s  0.00 %  0.00 % [rcuob/0]
    def getIoTopData(self):
        
        ioTopLines = self.client.getResponse('GetCmdIotop')
        ioTopResults = {}
        ioTopResults['topData'] = {}
        ioTopResults['rawResult'] = ioTopLines[:]
        
        dataLineStartingIndex = 0
        for line in ioTopLines:
            if (line.strip() == 'TID  PRIO  USER     DISK READ  DISK WRITE  SWAPIN      IO    COMMAND'):
                break
            else:
                dataLineStartingIndex += 1
        
        while(dataLineStartingIndex >= 0):
            ioTopLines.pop(0)
            dataLineStartingIndex -= 1

        orderIndex = 1
        for line in ioTopLines:
            # print (line)
            if (line.strip() == ''):
                continue

            # find the 'M/s" or 'B/s', they are for disk read and write
            matches = re.findall('\s*\d+\.\d{2}\s*[G|M|B]\/s\s+', line)
            diskRead = matches[0].strip()
            diskWrite = matches[1].strip()

            # find the "0.00 %" occurrences, they are for swapin and io
            matches = re.findall('\s*\d+\.\d{2}\s*\%\s+', line)
            swapin = matches[0].strip()
            io = matches[1].strip()
            
            lineValues = line.split()
            pid = lineValues[0].strip()
            prio = lineValues[1].strip()
            user = lineValues[2].strip()
            
            lastPercentIndex = line.rfind('%')
            command = line[lastPercentIndex+1:]

            ioTopItem = {}
            ioTopItem['TID'] = pid
            ioTopItem['PRIO'] = prio
            ioTopItem['USER'] = user
            ioTopItem['READ'] = diskRead
            ioTopItem['WRITE'] = diskWrite
            ioTopItem['SWAPIN'] = swapin
            ioTopItem['IO'] = io
            ioTopItem['COMMAND'] = command
        
            # use an incremental int as key, so we keey the order of the items.
            ioTopResults['topData'][orderIndex] = ioTopItem
            orderIndex += 1
        
        return ioTopResults


if( __name__ =='__main__' ):
    monitor = IOMonitor('www.linuxxueyuan.com')
    monitor.config = 'debug'

    pp = pprint.PrettyPrinter(indent=2)
    
    # monitor = IOMonitor('www.linuxep.com')
    # pp.pprint(monitor.getIoTopData())
    pp.pprint(monitor.getStatus())

    # to make a io change on server:  sudo dd if=/dev/sda of=/dev/null &




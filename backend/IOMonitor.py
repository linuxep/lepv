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
        responseLines = self.client.getResponse("GetCmdDf")
        if (len(responseLines) == 0):
            return {}
        
        responseData = {}
        responseData['rawResult'] = responseLines[:]

        diskData = {}
        for resultLine in responseLines:
            if (not resultLine.startswith('/dev/')):
                continue

            lineValues = resultLine.split()
            diskName = lineValues[0][5:]
            diskData[diskName] = {}
            diskData[diskName]['size'] = lineValues[1]
            diskData[diskName]['used'] = lineValues[2]
            diskData[diskName]['free'] = lineValues[3]

            diskData['size'] = lineValues[1]
            diskData['used'] = lineValues[2]
            diskData['free'] = lineValues[3]

        capacity = {}
        capacity['diskTotal'] = diskData['size']
        capacity['diskUsed'] = diskData['used']
        
        responseData['data'] = capacity
        return responseData


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

    def getIoPPData(self):

        ioTopLines = self.client.getResponse('GetCmdIopp')
        ioResults = {}
        ioResults['data'] = {}
        if (self.config == 'debug'):    
            ioResults['rawResult'] = ioTopLines[:]
        
        headerLine = ioTopLines.pop(0)
        # TODO: validate the header column ordering here.

        # pid    rchar    wchar    syscr    syscw   rbytes   wbytes  cwbytes command
        # 1        0        0        0        0        0        0        0 init
        # 2        0        0        0        0        0        0        0 kthreadd
        # 3        0        0        0        0        0        0        0 ksoftirqd/0
        # 5        0        0        0        0        0        0        0 kworker/0:0H
        orderIndex = 1
        for line in ioTopLines:
            # print (line)
            if (line.strip() == ''):
                continue

            lineValues = line.split()

            ioTopItem = {}
            ioTopItem['pid'] = lineValues.pop(0)
            ioTopItem['rchar'] = lineValues.pop(0)
            ioTopItem['wchar'] = lineValues.pop(0)
            ioTopItem['syscr'] = lineValues.pop(0)
            ioTopItem['syscw'] = lineValues.pop(0)
            ioTopItem['rbytes'] = lineValues.pop(0)
            ioTopItem['wbytes'] = lineValues.pop(0)
            ioTopItem['cwbytes'] = lineValues.pop(0)
            ioTopItem['command'] = ' '.join([str(x) for x in lineValues])

            # use an incremental int as key, so we keey the order of the items.
            ioResults['data'][orderIndex] = ioTopItem
            orderIndex += 1

        return ioResults


if( __name__ =='__main__' ):
    monitor = IOMonitor('www.linuxxueyuan.com')
    monitor.config = 'debug'

    pp = pprint.PrettyPrinter(indent=2)
    
    # monitor = IOMonitor('www.linuxep.com')
    # pp.pprint(monitor.getIoTopData())
    pp.pprint(monitor.getIoPPData())

    # to make a io change on server:  sudo dd if=/dev/sda of=/dev/null &




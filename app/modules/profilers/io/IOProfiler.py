"""Module for I/O related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import datetime
import pprint
import re

from modules.lepd.LepDClient import LepDClient


class IOProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        self.client = LepDClient(self.server)
        self.config = config

    def get_status(self):

        start_time = datetime.datetime.now()
        
        result = self.client.getIostatResult()

        if not result:
            return {}
        
        end_time = datetime.datetime.now()
        
        raw_results = result[:]
        
        headerline = result.pop(0)

        duration = "%.1f" % ((end_time - start_time).total_seconds())
        io_status = {
            'lepdDuration': duration,
            'disks': {},
            'diskCount': 0,
            'ratio': 0
        }

        for line in result:
            if (line.strip() == ""):
                continue

            line_values = line.split()

            device_name = line_values[0]
            io_status['diskCount'] += 1
            io_status['disks'][device_name] = {}

            io_status['disks'][device_name]['rkbs'] = line_values[5]
            io_status['disks'][device_name]['wkbs'] = line_values[6]
            io_status['disks'][device_name]['ratio'] = line_values[-1]
            
            this_disk_ratio = self.client.toDecimal(line_values[-1])
            if this_disk_ratio > io_status['ratio']:
                io_status['ratio'] = this_disk_ratio

        end_time_2 = datetime.datetime.now()
        duration = "%.1f" % ((end_time_2 - end_time).total_seconds())
        io_status['lepvParsingDuration'] = duration
        
        response_data = {
            'data': io_status,
            'rawResult': raw_results
        }
        return response_data
    
    def get_capacity(self):
        responseLines = self.client.getResponse("GetCmdDf")
        if (len(responseLines) == 0):
            return {}
        
        responseData = {}
        if (self.config == 'debug'):
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


    def get_io_top(self, ioTopLines = None):

        if (ioTopLines == None):
            ioTopLines = self.client.getResponse('GetCmdIotop')
        
        ioTopResults = {}
        ioTopResults['data'] = {}
        ioTopResults['rawResult'] = ioTopLines[:]
        # print(len(ioTopLines))
        if (len(ioTopLines) < 2):
            return ioTopResults

        
        dataLineStartingIndex = 0
        for line in ioTopLines:
            if (re.match(r'\W*TID\W+PRIO\W+USER\W+DISK READ\W+DISK WRITE\W+SWAPIN\W+IO\W+COMMAND\W*', line.strip(), re.M|re.I)):
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
            
            if (self.client.LEPDENDINGSTRING in line):
                break

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
            ioTopResults['data'][orderIndex] = ioTopItem
            orderIndex += 1
        
        return ioTopResults

if( __name__ =='__main__' ):
    profiler = IOProfiler('www.rmlink.cn')
    profiler.config = 'debug'

    pp = pprint.PrettyPrinter(indent=2)
    
    # monitor = IOMonitor('www.rmlink.cn')
    # pp.pprint(profiler.get_io_top())
    profiler.get_io_top()
    # pp.pprint(profiler.getIoPPData())

    # to make a io change on server:  sudo dd if=/dev/sda of=/dev/null &




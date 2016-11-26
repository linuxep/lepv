"""Module for memory related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from backend.LepDClient import LepDClient
from decimal import Decimal

__author__ = 'xmac'

class MemoryMonitor:

    def __init__(self, server, config='release'):
        self.server = server
        self.client = LepDClient(self.server)
        self.config = config
        
        self.dataCount = 25

    def convertKbToMb(self, strKbValue):
        return Decimal(int(strKbValue) / 1024).quantize(Decimal('0'))

    def getStatus(self):

        response = self.client.getResponse("GetProcMeminfo")
        if (response == None or len(response) == 0):
            return None

        responseData = {}
        if (self.config == 'debug'):
            responseData['rawResult'] = response[:]
        
        results = {}
        for line in response:
            linePairs = line.split(":")
            lineKey = linePairs[0].strip()
            lineValue = linePairs[1].replace('kB', '').strip()

            results[lineKey] = lineValue

        componentInfo = {}
        componentInfo["name"] = "memory"

        componentInfo['total'] = Decimal(int(results['MemTotal']) / 1024).quantize(Decimal('0'))
        componentInfo['free'] = Decimal(int(results['MemFree']) / 1024).quantize(Decimal('0'))
        componentInfo['buffers'] = Decimal(int(results['Buffers']) / 1024).quantize(Decimal('0'))
        componentInfo['cached'] = Decimal(int(results['Cached']) / 1024).quantize(Decimal('0'))
        componentInfo['used'] = componentInfo['total'] - componentInfo['free'] - componentInfo['buffers'] - componentInfo['cached']

        usedRatio = (componentInfo['used'] / componentInfo['total']) * 100
        #usedRatio = Decimal(usedRatio).quantize(Decimal('0.00'))
        usedRatio = ("%.2f" % usedRatio)
        componentInfo["ratio"] = usedRatio

        componentInfo['unit'] = 'MB'
        
        responseData['data'] = componentInfo
        return responseData

    def getCapacity(self):
        response = self.client.getProcMeminfo()

        if (not response):
            return None

        componentInfo = {}
        componentInfo["name"] = "memory"
        componentInfo["capacity"] = int(int(response['MemTotal']) / 1024)
        componentInfo["unit"] = "MB"
        
        componentInfo["summary"] = str(componentInfo["capacity"]) + " " + componentInfo["unit"]

        return componentInfo

    def normalizeValue(self, valueString):
        # 1.23% -> 0.012
        if (valueString.endswith("%")):
            valueString = valueString.replace("%", "")
            valueString = Decimal(Decimal(valueString) / 100).quantize(Decimal('0.0000'))
        elif (valueString == "N/A"):
            valueString = 0
        
        return valueString
        
    def getMemoryStat(self):

        memoryStatData = {}
        
        results = self.client.getResponse('GetCmdSmem')
        if (self.config == 'debug'):
            memoryStatData['rawResult'] = results[:]

        headerLine = results.pop(0)
        headers = headerLine.split()
        
        # sMemInfo['headerLine'] = headerLine
        for line in results:
            # print(line)
            lineValues = line.split()

            pid = lineValues[0]
            memoryStatData[pid] = {}
            # sMemInfo['line'] = line
            memoryStatData[pid]['pid'] = lineValues.pop(0)
            memoryStatData[pid]['user'] = lineValues.pop(0)

            # the command section is likely to have whitespaces in it thus hard to locate it. workaround here.
            memoryStatData[pid]['rss'] = self.normalizeValue(lineValues.pop())
            memoryStatData[pid]['pss'] = self.normalizeValue(lineValues.pop())
            memoryStatData[pid]['uss'] = self.normalizeValue(lineValues.pop())
            memoryStatData[pid]['swap'] = self.normalizeValue(lineValues.pop())

            memoryStatData[pid]['command'] = ' '.join([str(x) for x in lineValues])

            if(len(memoryStatData) >= self.dataCount):
                break

        return memoryStatData

    def getMeminfo(self):
        return self.client.getProcMeminfo()

    # def getSmemOutput(self):
    #     response = self.client.getSmemOutput()
    #     return response



if( __name__ =='__main__' ):
    monitor = MemoryMonitor('www.linuxxueyuan.com')
    monitor.config = 'debug'
    # monitor = MemoryMonitor('www.linuxep.com')
    # monitor.getMemoryStat()
    print(monitor.getStatus())
    # print(monitor.getSmemOutput())
    # print(monitor.getProcrankOutput())
    # 
    # print(monitor.getCapacity())


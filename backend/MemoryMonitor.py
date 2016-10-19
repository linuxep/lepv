"""Module for memory related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from backend.LepDClient import LepDClient
from decimal import Decimal

__author__ = 'xmac'

class MemoryMonitor:

    def __init__(self, server):
        self.server = server
        self.client = LepDClient(self.server)

    def convertKbToMb(self, strKbValue):
        return Decimal(int(strKbValue) / 1024).quantize(Decimal('0'))

    def getStatus(self):
        response = self.client.getProcMeminfo()

        componentInfo = {}
        if (response == None):
            componentInfo['error'] = 'timeout'
            return componentInfo
        
        componentInfo["name"] = "memory"

        componentInfo['total'] = Decimal(int(response['MemTotal']) / 1024).quantize(Decimal('0'))
        componentInfo['free'] = Decimal(int(response['MemFree']) / 1024).quantize(Decimal('0'))
        componentInfo['buffers'] = Decimal(int(response['Buffers']) / 1024).quantize(Decimal('0'))
        componentInfo['cached'] = Decimal(int(response['Cached']) / 1024).quantize(Decimal('0'))
        componentInfo['used'] = componentInfo['total'] - componentInfo['free'] - componentInfo['buffers'] - componentInfo['cached']

        usedRatio = (componentInfo['used'] / componentInfo['total']) * 100
        #usedRatio = Decimal(usedRatio).quantize(Decimal('0.00'))
        usedRatio = ("%.2f" % usedRatio)
        componentInfo["ratio"] = usedRatio

        componentInfo['unit'] = 'MB'
        return componentInfo

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
        
        results = self.client.getSMem()

        headerLine = results.pop(0)
        print(headerLine)
        headers = headerLine.split()

        sMemInfo = {}
        # sMemInfo['headerLine'] = headerLine
        for line in results:
            print(line)
            lineValues = line.split()

            pid = lineValues[0]
            sMemInfo[pid] = {}
            # sMemInfo['line'] = line
            sMemInfo[pid]['pid'] = lineValues.pop(0)
            sMemInfo[pid]['user'] = lineValues.pop(0)

            # the command section is likely to have whitespaces in it thus hard to locate it. workaround here.
            sMemInfo[pid]['rss'] = self.normalizeValue(lineValues.pop())
            sMemInfo[pid]['pss'] = self.normalizeValue(lineValues.pop())
            sMemInfo[pid]['uss'] = self.normalizeValue(lineValues.pop())
            sMemInfo[pid]['swap'] = self.normalizeValue(lineValues.pop())

            sMemInfo[pid]['command'] = ' '.join([str(x) for x in lineValues])

            if(len(sMemInfo) >= 25):
                break

        return sMemInfo

    def getMeminfo(self):
        return self.client.getProcMeminfo()

    def getSmemOutput(self):
        response = self.client.getSmemOutput()
        return response

    def getProcrankOutput(self):
        response = self.client.getProcrankOutput()
        return response


if( __name__ =='__main__' ):
    monitor = MemoryMonitor('www.linuxxueyuan.com')
    # monitor = MemoryMonitor('www.linuxep.com')
    # monitor.getMemoryStat()
    print(monitor.getStatus())
    # print(monitor.getSmemOutput())
    # print(monitor.getProcrankOutput())
    # 
    # print(monitor.getCapacity())


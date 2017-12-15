"""Module for memory related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import pprint
import re
from decimal import Decimal

from modules.lepd.LepDClient import LepDClient

__author__ = 'xmac'


class MemoryProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        self.client = LepDClient(self.server)
        self.config = config
        
        self.dataCount = 25

    def convertKbToMb(self, strKbValue):
        return Decimal(int(strKbValue) / 1024).quantize(Decimal('0'))

    def getStatus(self, response_lines=None):

        lepd_command = "GetProcMeminfo"

        print("     calling LEPD by: " + lepd_command)
        if not response_lines:
            response_lines = self.client.getResponse(lepd_command)
        elif isinstance(response_lines, str):
            response_lines = self.client.split_to_lines(response_lines)
        print('     ' + lepd_command + " returned")

        response_data = {}
        if self.config == 'debug':
            response_data['rawResult'] = response_lines[:]
            response_data['lepd_command'] = lepd_command

        if len(response_lines) == 0:
            return response_data
        
        results = {}
        for line in response_lines:
            linePairs = line.split(":")
            lineKey = linePairs[0].strip()
            lineValue = linePairs[1].replace('kB', '').strip()

            results[lineKey] = lineValue

        componentInfo = {}
        componentInfo["name"] = "memory"

        componentInfo['total'] = self.client.toDecimal(Decimal(int(results['MemTotal']) / 1024).quantize(Decimal('0')))
        componentInfo['free'] = self.client.toDecimal(Decimal(int(results['MemFree']) / 1024).quantize(Decimal('0')))
        componentInfo['buffers'] = self.client.toDecimal(Decimal(int(results['Buffers']) / 1024).quantize(Decimal('0')))
        componentInfo['cached'] = self.client.toDecimal(Decimal(int(results['Cached']) / 1024).quantize(Decimal('0')))
        componentInfo['used'] = componentInfo['total'] - componentInfo['free'] - componentInfo['buffers'] - componentInfo['cached']

        usedRatio = (componentInfo['used'] / componentInfo['total']) * 100
        #usedRatio = Decimal(usedRatio).quantize(Decimal('0.00'))
        usedRatio = ("%.2f" % usedRatio)
        componentInfo["ratio"] = usedRatio

        componentInfo['unit'] = 'MB'

        response_data['data'] = componentInfo
        return response_data

    def getCapacity(self, sampleDataLines = None):
        responseLines = []
        if (sampleDataLines == None):
            responseLines = self.client.getResponse("GetProcMeminfo")
        else:
            responseLines = sampleDataLines
            
        if (len(responseLines) == 0):
            return {}
        
        responseData = {}
        if (self.config == 'debug'):
            responseData['rawResult'] = responseLines[:]

        results = {}
        for line in responseLines:
            # print(line)
            if (self.client.LEPDENDINGSTRING in line):
                continue
                
            linePairs = line.split(":")
            lineKey = linePairs[0].strip()
            lineValue = linePairs[1].replace('kB', '').strip()

            results[lineKey] = lineValue

        componentInfo = {}
        componentInfo["name"] = "memory"
        componentInfo["capacity"] = int(int(results['MemTotal']) / 1024)
        componentInfo["unit"] = "MB"
        
        componentInfo["summary"] = str(componentInfo["capacity"]) + " " + componentInfo["unit"]
        
        responseData['data'] = componentInfo
        return responseData

    def normalizeValue(self, valueString):
        # 1.23% -> 0.012
        if (valueString.endswith("%")):
            valueString = valueString.replace("%", "")
            valueString = Decimal(Decimal(valueString) / 100).quantize(Decimal('0.0000'))
        elif (valueString == "N/A"):
            valueString = 0
        
        return valueString
        
    # def getMemoryStat(self):
    # 
    #     memoryStatData = {}
    #     
    #     results = self.client.getResponse('GetCmdSmem')
    #     if (self.config == 'debug'):
    #         memoryStatData['rawResult'] = results[:]
    # 
    #     headerLine = results.pop(0)
    #     headers = headerLine.split()
    #     
    #     # sMemInfo['headerLine'] = headerLine
    #     for line in results:
    #         # print(line)
    #         lineValues = line.split()
    # 
    #         pid = lineValues[0]
    #         memoryStatData[pid] = {}
    #         # sMemInfo['line'] = line
    #         memoryStatData[pid]['pid'] = lineValues.pop(0)
    #         memoryStatData[pid]['user'] = lineValues.pop(0)
    # 
    #         # the command section is likely to have whitespaces in it thus hard to locate it. workaround here.
    #         memoryStatData[pid]['rss'] = self.normalizeValue(lineValues.pop())
    #         memoryStatData[pid]['pss'] = self.normalizeValue(lineValues.pop())
    #         memoryStatData[pid]['uss'] = self.normalizeValue(lineValues.pop())
    #         memoryStatData[pid]['swap'] = self.normalizeValue(lineValues.pop())
    # 
    #         memoryStatData[pid]['command'] = ' '.join([str(x) for x in lineValues])
    # 
    #         if(len(memoryStatData) >= self.dataCount):
    #             break
    # 
    #     return

    def getProcrank(self):

        procrankData = {}

        resultLines = self.client.getResponse('GetCmdProcrank')
        if (len(resultLines) == 0):
            return {}
        
        if (self.config == 'debug'):
            procrankData['rawResult'] = resultLines[:]

        procrankData['data'] = {}
        procrankData['data']['procranks'] = {}
        headerLine = resultLines.pop(0)
        lineIndex = 0
        
        for line in resultLines:
            if (re.match( r'\W+-+\W+-+\W-+.*', line, re.M|re.I)):
                break
            lineValues = line.split()

            procrankData['data']['procranks'][lineIndex] = {}
            procrankData['data']['procranks'][lineIndex]['pid'] = lineValues.pop(0)
            procrankData['data']['procranks'][lineIndex]['vss'] = self.client.toDecimal(Decimal(Decimal(lineValues.pop(0)[:-1])))
            procrankData['data']['procranks'][lineIndex]['rss'] = self.client.toDecimal(Decimal(Decimal(lineValues.pop(0)[:-1])))
            procrankData['data']['procranks'][lineIndex]['pss'] = self.client.toDecimal(Decimal(Decimal(lineValues.pop(0)[:-1])))
            procrankData['data']['procranks'][lineIndex]['uss'] = self.client.toDecimal(Decimal(Decimal(lineValues.pop(0)[:-1])))

            procrankData['data']['procranks'][lineIndex]['cmdline'] = ' '.join([str(x) for x in lineValues])
            
            lineIndex += 1

            if(len(procrankData) >= self.dataCount):
                break
        
        # now parse from end, which contains summary info
        lastLine = resultLines[-1]
        procrankData['data']['sum'] = {}
        if (lastLine.startswith('RAM:')):
            lastLine = lastLine.replace("RAM:", '')
            lastLineValuePairs = lastLine.split(", ")
            for valuePair in lastLineValuePairs:
                keyValuePair = valuePair.split()
                
                keyName = keyValuePair[1].strip()
                keyValue = keyValuePair[0].strip()

                procrankData['data']['sum'][keyName + "Unit"] = keyValue[-1:]
                procrankData['data']['sum'][keyName] = self.client.toDecimal(Decimal(Decimal(keyValue[:-1])))

        xssSumLine = resultLines[-3].strip()
        if (xssSumLine.endswith('TOTAL')):
            xssValues = xssSumLine.split()
            
            ussTotalString = xssValues[-2]
            procrankData['data']['sum']['ussTotalUnit'] = ussTotalString[-1:]
            procrankData['data']['sum']['ussTotal'] = self.client.toDecimal(Decimal(Decimal(ussTotalString[:-1])))
            
            pssTotalString = xssValues[-3]
            procrankData['data']['sum']['pssTotalUnit'] = pssTotalString[-1:]
            procrankData['data']['sum']['pssTotal'] = self.client.toDecimal(Decimal(Decimal(pssTotalString[:-1])))
            
        return procrankData


if( __name__ =='__main__' ):
    pp = pprint.PrettyPrinter(indent=2)

    profiler = MemoryProfiler('www.rmlink.cn')
    profiler.config = 'debug'

    i = 1
    while i < 100:
        print(i)
        status = profiler.getStatus()
        if status:
            print("YES")
        else:
            print("NO!!!!!!!!!!!")
        i += 1
        print("")
    # pp.pprint(profiler.getProcrank())
    # print(profiler.getSmemOutput())
    # print(profiler.getProcrankOutput())
    # 
    # print(profiler.get_capacity())


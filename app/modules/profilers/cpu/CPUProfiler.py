"""Module for CPU related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import pprint
import re
from decimal import Decimal

from modules.lepd.LepDClient import LepDClient


class CPUProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        self.client = LepDClient(self.server)
        self.config = config
        
        # this maxDataCount should match the one defined for UI.
        self.maxDataCount = 25
    
    def getCpuInfoForArm(self, lines):

        results = {}

        line = lines.pop(0)
        results['architecture'] = "ARM"
        results['model name'] = line.split(':')[1].strip()
        results['processors'] = {}

        line = lines.pop(0)
        while(not line.startswith("Features")):
            if (line.startswith("processor")):

                processorId = line.split(":")[1].strip()
                results['processors'][processorId] = {}

                bogoMips = lines.pop(0).split(":")[1].strip()
                results['processors'][processorId]["processorId"] = processorId
                results['processors'][processorId]["bogomips"] = bogoMips
            
            line = lines.pop(0)

        return results

    def getCpuInfoForArmArch64(self, lines):

        results = {}

        line = lines.pop(0)
        results['architecture'] = "ARM"
        
        results['model name'] = line.split(":")[1].strip()
        results['processors'] = {}

        line = lines.pop(0)
        while(not line.startswith("Features")):
            if (line.startswith("processor")):

                processorId = line.split(":")[1].strip()
                results['processors'][processorId] = {}
                results['processors'][processorId]["processorId"] = processorId
                results['processors'][processorId]["bogomips"] = ''

            line = lines.pop(0)

        return results
    
    def getCpuInfoForX86(self, lines):

        results = {}
        results['architecture'] = "X86"
        results['processors'] = {}
        
        for line in lines:
            if (line.strip() == ""):
                continue
    
            if re.match(r'processor\W+:\W+\d.*', line, re.M|re.I):
                linePairs = line.split(":")
                processorId = linePairs[1].strip()
                results['processors'][processorId] = {}
                continue
    
            if (":" in line):
                linePairs = line.split(":")
                lineKey = linePairs[0].strip()
                lineValue = ''
                if (len(linePairs) > 1):
                    lineValue = linePairs[1].strip()

                results['processors'][processorId][lineKey] = lineValue
    
        return results
    
    def getCpuInfo(self, cpuInfoLines = None):
        
        if (cpuInfoLines == None):
            cpuInfoLines = self.client.getResponse('GetProcCpuinfo')
            
        responseData = {}
        if (self.config == 'debug'):
            responseData['rawResult'] = cpuInfoLines

        firstLine = cpuInfoLines[0]
        if ("ARM" in firstLine):
            responseData['data'] = self.getCpuInfoForArm(cpuInfoLines)
        elif ('AArch64' in firstLine):
            responseData['data'] = self.getCpuInfoForArmArch64(cpuInfoLines)
        else:
            secondLine = cpuInfoLines[1]
            responseData['data'] = self.getCpuInfoForX86(cpuInfoLines)
            if ('GenuineIntel' not in secondLine):
                responseData['data']['architecture'] = 'ARM'

        responseData['data']['processorCount'] = 0
        for line in cpuInfoLines:
            if re.match(r'\W*processor\W*:\W*\d+', line, re.M|re.I):
                responseData['data']['processorCount'] += 1
        
        return responseData

    def getProcessorCount(self, cpuInfoLines = None):

        if (cpuInfoLines == None):
            cpuInfoLines = self.client.getResponse('GetCpuInfo')

        responseData = {}
        for line in cpuInfoLines:
            if line.startswith('cpunr'):
                responseData['count'] = int(line.split(":")[1].strip())
                break

        if ('count' not in responseData):
            print('failed in getting processor count by GetCpuInfo')
            print(cpuInfoLines)
            
        return responseData

    def getCapacity(self):
        
        cpuInfoData = self.getCpuInfo()
        
        if (not cpuInfoData):
            return {}

        responseData = {}
        if (self.config == 'debug'):
            responseData['rawResult'] = cpuInfoData['rawResult']
            responseData['lepd_command'] = 'GetProcCpuinfo'
        
        capacity = {}
        capacity['processors'] = cpuInfoData['data']['processors']

        coresString = 'Core'
        coreCount = len(cpuInfoData['data']['processors'])
        capacity['coresCount'] = coreCount
        
        if (coreCount > 1):
            coresString = "Cores"

        for processorId, processorData in cpuInfoData['data']['processors'].items():
            
            if (cpuInfoData['data']['architecture'] == "ARM"):
                if ('model name' in cpuInfoData['data']):
                    processorData['model'] = cpuInfoData['data']['model name']
                else:
                    processorData['model'] = ''

                # Summary is a string to briefly describe the CPU, like "2GHZ x 2", meaning it's a 2-core cpu with 2GHZ speed.
                if ('bogomips' not in processorData):
                    capacity['bogomips'] = ''
                    capacity['summary'] = ''
                else:
                    capacity['bogomips'] = processorData['bogomips']
                    capacity['summary'] = processorData['bogomips'] + " MHz x " + str(coreCount) + coresString
                    
                capacity['model'] = processorData['model']
                capacity['architecture'] = 'ARM'
            
            else:
                modelName = processorData['model name'].replace("(R)", "").replace(" CPU", "")
                if (" @" in modelName):
                    modelName = modelName[0:modelName.find(" @")]
                processorData['model'] = modelName
                
                processorSpeed = Decimal(processorData['cpu MHz']).quantize(Decimal('0'))
                
                # Summary is a string to briefly describe the CPU, like "2GHZ x 2", meaning it's a 2-core cpu with 2GHZ speed.
                capacity['summary'] = str(processorSpeed) + " MHz x " + str(coreCount) + coresString
                capacity['model'] = modelName
                capacity['bogomips'] = processorData['bogomips']
                capacity['architecture'] = 'X86'
            
            break
        
        responseData['data'] = capacity
        return responseData

    def getStatus(self):

        statData = self.get_stat()
        allIdleRatio = self.client.toDecimal(statData['data']['all']['idle'])

        componentInfo = {}
        componentInfo["name"] = "cpu"
        componentInfo["ratio"] = 100 - allIdleRatio
        componentInfo['server'] = self.server
        
        if (self.config == 'debug'):
            componentInfo['rawResult'] = statData['rawResult']

        return componentInfo

    def get_stat(self):

        results = self.client.getCmdMpStat()
        if not results:
            return None
        results.pop(0)

        # Basic data, basically for debugging
        stat_data = {
            "lepd_command": "GetCmdMpstat",
            "rawResult": results,
            "server": self.server
        }

        # Core data, for displaying
        stat_data['data'] = {}
        for line in results:
            
            if (line.strip() == ''):
                break
            
            line_values = line.split()

            cpu_stat = {}
            cpu_stat['idle'] = self.client.toDecimal(line_values[-1])
            cpu_stat['gnice'] = self.client.toDecimal(line_values[-2])
            cpu_stat['guest'] = self.client.toDecimal(line_values[-3])
            cpu_stat['steal'] = self.client.toDecimal(line_values[-4])
            cpu_stat['soft'] = self.client.toDecimal(line_values[-5])
            cpu_stat['irq'] = self.client.toDecimal(line_values[-6])
            cpu_stat['iowait'] = self.client.toDecimal(line_values[-7])
            cpu_stat['system'] = self.client.toDecimal(line_values[-8])
            cpu_stat['nice'] = self.client.toDecimal(line_values[-9])
            cpu_stat['user'] = self.client.toDecimal(line_values[-10])

            cpu_name = line_values[-11]
            stat_data['data'][cpu_name] = cpu_stat

        # TODO: Analysis data, for notification and alert
        stat_data['message'] = {
            '0': {
                'error': '',
                'warning': 'Load NOT balanced, this core is over loaded!',
                'info': ''
            },
            '1': {
                'error': '',
                'warning': 'Load NOT balanced, this core is over idled!',
                'info': ''
            }
        }

        return stat_data

    def get_average_load(self, options={}):
        response_lines = self.client.getResponse('GetProcLoadavg')

        response_data = {}
        # if options['debug']:
        #     response_data['rawResult'] = response_lines[:]
        #     response_data['lepd_command'] = 'GetProcLoadavg'
        
        response = response_lines[0].split(" ")

        # '0.00 0.01 0.05 1/103 24750
        # 'avg system load of 1 minute ago, 5 minutes ago, 15 minutes ago,
        # the fourth is A/B, A is the number of running processes
        # B is the total process count.
        # last number, like 24750 is the ID of the most recently running process.
        result_data = {
            'last1': self.client.toDecimal(response[0]),
            'last5': self.client.toDecimal(response[1]),
            'last15': self.client.toDecimal(response[2])
        }

        response_data['data'] = result_data
        
        return response_data

    def getTopOutput(self, responseLines = None):

        if (responseLines == None):
            responseLines = self.client.getResponse('GetCmdTop')

        if (len(responseLines) == 0):
            return {}
        
        responseData = {}
        if (self.config == 'debug'):
            responseData['rawResult'] = responseLines[:]
        
        headerLine = responseLines.pop(0)
        while ( not re.match(r'\W*PID\W+USER\W+.*', headerLine, re.M|re.I) ):
            headerLine = responseLines.pop(0)

        headerColumns = headerLine.split()

        result = {}

        for lineIndex, responseLine in enumerate(responseLines):
            if (self.client.LEPDENDINGSTRING in responseLine):
                break
            
            if (lineIndex > self.maxDataCount):
                break
 
            lineValues = responseLine.split()

            result[lineIndex] = {}

            # print(headerLine)
            for columnIndex, columnName in enumerate(headerColumns):
                if (columnName == 'Name' or columnName == 'CMD'):
                    result[lineIndex][columnName] = ' '.join([str(x) for x in lineValues[columnIndex:]])
                else:
                    result[lineIndex][columnName] = lineValues[columnIndex]

        responseData['data'] = {}
        responseData['data']['top'] = result
        responseData['data']['headerline'] = headerLine
        
        if (re.match(r'\W*PID\W+USER\W+PR\W+.*', headerLine, re.M|re.I)):
            # android :
            #   PID USER     PR  NI CPU% S  #THR     VSS     RSS PCY Name
            responseData['data']['os'] = 'android'
        elif (re.match(r'\W*PID\W+USER\W+PRI\W+NI\W+VSZ\W+RSS\W+.*', headerLine, re.M|re.I)):
            # for Linux:
            # PID USER     PRI  NI    VSZ   RSS S %CPU %MEM     TIME CMD
            responseData['data']['os'] = 'linux'
        else:
            print("GetCmdTop command returned data from unrecognized system")
        
        return responseData

if( __name__ =='__main__' ):
    
    # run "stress" command on the server to make data change
    # stress -c 2 -i 1 -m 1 --vm-bytes 128M -t 30s
    # mpstat -P ALL

    pp = pprint.PrettyPrinter(indent=2)
    
    profiler = CPUProfiler('www.rmlink.cn')

    pp.pprint(profiler.getCapacity())
    pp.pprint(profiler.getProcessorCount())
    # pp.pprint(profiler.getStat())
    # pp.pprint(profiler.getAverageLoad())
    # pp.pprint(profiler.getTopOutput())
    # pp.pprint(profiler.getCpuByName("kworker/u3:0"))
    # pp.pprint(profiler.getCpuByPid("4175"))
    # pp.pprint(profiler.getTopHResult())

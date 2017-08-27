"""Module for CPU related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from decimal import Decimal
import re
import pprint

from app.monitors.LepDClient import LepDClient

class CPUMonitor:

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

        statData = self.getStat()
        allIdleRatio = self.client.toDecimal(statData['data']['all']['idle'])

        componentInfo = {}
        componentInfo["name"] = "cpu"
        componentInfo["ratio"] = 100 - allIdleRatio
        componentInfo['server'] = self.server
        
        if (self.config == 'debug'):
            componentInfo['rawResult'] = statData['rawResult']

        return componentInfo

    def getStat(self):

        results = self.client.getCmdMpStat()
        if (results == None):
            return None

        statData = {}
        
        results.pop(0)
        statData['rawResult'] = results
        
        statData['data'] = {}
        for line in results:
            
            if (line.strip() == ''):
                break
            
            lineValues = line.split()

            cpuStat = {}
            cpuStat['idle'] = self.client.toDecimal(lineValues[-1])
            cpuStat['gnice'] = self.client.toDecimal(lineValues[-2])
            cpuStat['guest'] = self.client.toDecimal(lineValues[-3])
            cpuStat['steal'] = self.client.toDecimal(lineValues[-4])
            cpuStat['soft'] = self.client.toDecimal(lineValues[-5])
            cpuStat['irq'] = self.client.toDecimal(lineValues[-6])
            cpuStat['iowait'] = self.client.toDecimal(lineValues[-7])
            cpuStat['system'] = self.client.toDecimal(lineValues[-8])
            cpuStat['nice'] = self.client.toDecimal(lineValues[-9])
            cpuStat['user'] = self.client.toDecimal(lineValues[-10])

            cpuName = lineValues[-11]
            statData['data'][cpuName] = cpuStat
        
        statData['server'] = self.server
        
        return statData

    def getAverageLoad(self):
        responseLines = self.client.getResponse('GetProcLoadavg')

        responseData = {}
        if (self.config == 'debug'):
            responseData['rawResult'] = responseLines[:]
        
        response = responseLines[0].split(" ")

        # '0.00 0.01 0.05 1/103 24750
        # 'avg system load of 1 minute ago, 5 minutes ago, 15 minutes ago,
        # the fourth is A/B, A is the number of running processes
        # B is the total process count.
        # last number, like 24750 is the ID of the most recently running process.
        resultData = {}
        resultData['last1'] = self.client.toDecimal(response[0])
        resultData['last5'] = self.client.toDecimal(response[1])
        resultData['last15'] = self.client.toDecimal(response[2])

        responseData['data'] = resultData
        
        return responseData

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
    
    monitor = CPUMonitor('www.linuxxueyuan.com')

    # pp.pprint(monitor.getCapacity())
    # pp.pprint(monitor.getProcessorCount())
    pp.pprint(monitor.getStat())
    # pp.pprint(monitor.getAverageLoad())
    # pp.pprint(monitor.getTopOutput())
    # pp.pprint(monitor.getCpuByName("kworker/u3:0"))
    # pp.pprint(monitor.getCpuByPid("4175"))
    # pp.pprint(monitor.getTopHResult())

"""Module for CPU related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from decimal import Decimal
from backend.LepDClient import LepDClient
import re
import pprint

class CPUMonitor:

    def __init__(self, server, config='release'):
        self.server = server
        self.client = LepDClient(self.server)
        self.config = config
    
    def getCpuInfoForArm(self, result):

        results = {}

        lines = result.split("\n")

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
    
    def getCpuInfoForX86(self, result):

        results = {}
        results['architecture'] = "X86"
        results['processors'] = {}
        
        lines = result.split("\n")
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
    
    def getCpuInfo(self):

        cpuInfoResult = self.client.getProcCpuinfo()
        if ("ARM" in cpuInfoResult):
            return self.getCpuInfoForArm(cpuInfoResult)
        else:
            return self.getCpuInfoForX86(cpuInfoResult)

    def getCapacity(self):
        
        processorsData = self.getCpuInfo()
        
        if (not processorsData):
            return {}
        
        capacity = {}
        capacity['processors'] = processorsData['processors']

        coresString = 'Core'
        coreCount = len(processorsData['processors'])
        capacity['coresCount'] = coreCount
        
        if (coreCount > 1):
            coresString = "Cores"

        for processorId, processorData in processorsData['processors'].items():
            
            if (processorsData['architecture'] == "ARM"):
                processorData['model'] = processorsData['model name']

                # Summary is a string to briefly describe the CPU, like "2GHZ x 2", meaning it's a 2-core cpu with 2GHZ speed.
                capacity['summary'] = processorData['bogomips'] + " MHz x " + str(coreCount) + coresString
                capacity['model'] = processorData['model']
                capacity['bogomips'] = processorData['bogomips']
            
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
            
            break

        return capacity

    def getStatus(self):

        statData = self.getStat()
        allIdleRatio = Decimal(statData['data']['all']['idle'])

        componentInfo = {}
        componentInfo["name"] = "cpu"
        componentInfo["ratio"] = 100 - allIdleRatio
        componentInfo['server'] = self.server

        return componentInfo

    def getStat(self):

        results = self.client.getCmdMpStat()
        if (results == None):
            return None

        results.pop(0)
        # for line in results:
        #     print(line)

        statData = {}
        statData['data'] = {}
        for line in results:
            
            if (line.strip() == ''):
                break
            
            lineValues = line.split()

            cpuStat = {}
            cpuStat['idle'] = lineValues[-1]
            cpuStat['gnice'] = lineValues[-2]
            cpuStat['guest'] = lineValues[-3]
            cpuStat['steal'] = lineValues[-4]
            cpuStat['soft'] = lineValues[-5]
            cpuStat['irq'] = lineValues[-6]
            cpuStat['iowait'] = lineValues[-7]
            cpuStat['system'] = lineValues[-8]
            cpuStat['nice'] = lineValues[-9]
            cpuStat['user'] = lineValues[-10]
            cpuStat['name'] = lineValues[-11]

            cpuName = lineValues[-11]
            statData['data'][cpuName] = cpuStat
        
        statData['server'] = self.server
        
        return statData

    def getAverageLoad(self):
        response = self.client.getAverageLoad()

        # '0.00 0.01 0.05 1/103 24750
        # 'avg system load of 1 minute ago, 5 minutes ago, 15 minutes ago,
        # the fourth is A/B, A is the number of running processes
        # B is the total process count.
        # last number, like 24750 is the ID of the most recently running process.
        resultData = {}
        resultData['last1'] = Decimal(response[0])
        resultData['last5'] = Decimal(response[1])
        resultData['last15'] = Decimal(response[2])

        return resultData

    def getTopOutput(self):
        response = self.client.getTopOutput()
        return response

    def getTopHResult(self):
        response = self.client.getTopHResult()
        return response

    def getCpuByName(self, name):
        response = self.client.getTopOutput()
        
        for line in response:
            if name in line:
                pid = line.strip().split(" ")[0].strip()
                cpu = re.search(" .\.. ", line).group().strip()
                return (pid, cpu)
        return None

    def getCpuByPid(self, pid):
        response = self.client.getTopOutput()
        
        for line in response:
            if pid == line.strip().split(" ")[0].strip():
                name = re.split(":.+ ",line, 1)[1].strip()
                cpu = re.search(" .\.. ", line).group().strip()
                return (name, cpu)
        return None

if( __name__ =='__main__' ):
    
    # run "stress" command on the server to make data change
    # stress -c 2 -i 1 -m 1 --vm-bytes 128M -t 30s
    # mpstat -P ALL

    pp = pprint.PrettyPrinter(indent=2)
    
    monitor = CPUMonitor('www.linuxxueyuan.com')
    # monitor = CPUMonitor('www.linuxep.com')

    pp.pprint(monitor.getCapacity())
    pp.pprint(monitor.getCpuInfo())
    # pp.pprint(monitor.getStat())
    # pp.pprint(monitor.getAverageLoad())
    # pp.pprint(monitor.getTopOutput())
    # pp.pprint(monitor.getCpuByName("kworker/u3:0"))
    # pp.pprint(monitor.getCpuByPid("4175"))
    # pp.pprint(monitor.getTopHResult())

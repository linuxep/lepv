"""Module for CPU related data parsing"""

__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import pprint
import re
from decimal import Decimal
from time import gmtime, strftime

from modules.lepd.LepDClient import LepDClient


class CPUProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        self.client = LepDClient(self.server)
        self.config = config
        
        # this maxDataCount should match the one defined for UI.
        self.maxDataCount = 25

        self.loadBalanceBenchMark = Decimal(40)
    
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

        lepd_command = 'GetProcCpuinfo'
        if (cpuInfoLines == None):
            cpuInfoLines = self.client.getResponse(lepd_command)
            
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

        lepd_command = 'GetCpuInfo'
        if (cpuInfoLines == None):
            cpuInfoLines = self.client.getResponse(lepd_command)

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

    def get_status(self):

        statData = self.get_irq()
        allIdleRatio = self.client.toDecimal(statData['data']['all']['idle'])

        responseData = {}
        responseData["data"] = {}

        componentInfo = {}
        componentInfo["name"] = "cpu"
        componentInfo["ratio"] = 100 - allIdleRatio
        componentInfo['server'] = self.server
        
        if (self.config == 'debug'):
            componentInfo['rawResult'] = statData['rawResult']

        responseData["data"] = componentInfo

        return responseData

    def get_irq(self, response_lines=[]):

        lepd_command = 'GetCmdMpstat'
        if not response_lines:
            response_lines = self.client.getResponse(lepd_command)
        elif isinstance(response_lines, str):
            response_lines = self.client.split_to_lines(response_lines)

        # discard the first three lines
        response_lines.pop(0)
        response_lines.pop(0)
        response_lines.pop(0)

        irq_data = {}
        irq_data['data'] = {}

        for line in response_lines:
            
            if (line.strip() == ''):
                break
            
            line_values = line.split()

            irq_stat = {}
            try:
                irq_stat['idle'] = float(line_values[-1])
                irq_stat['gnice'] = float(line_values[-2])
                irq_stat['guest'] = float(line_values[-3])
                irq_stat['steal'] = float(line_values[-4])
                irq_stat['soft'] = float(line_values[-5])
                irq_stat['irq'] = float(line_values[-6])
                irq_stat['iowait'] = float(line_values[-7])
                irq_stat['system'] = float(line_values[-8])
                irq_stat['nice'] = float(line_values[-9])
                irq_stat['user'] = float(line_values[-10])

                cpu_name = line_values[-11]
            except Exception as err:
                print(err)
                continue

            irq_data['data'][cpu_name] = irq_stat

        return irq_data

    def get_softirq(self, response_lines=[]):

        lepd_command = 'GetCmdMpstat-I'
        if not response_lines:
            response_lines = self.client.getResponse(lepd_command)
        elif isinstance(response_lines, str):
            response_lines = self.client.split_to_lines(response_lines)

        # discard the first two lines
        response_lines.pop(0)
        response_lines.pop(0)

        softirq_resp = []
        softirq_data = {}
        softirq_data['data'] = {}

        # print(response_lines)
        startIndex = 0
        for line in response_lines:
            if (line.strip() == ''):
                startIndex = startIndex + 1

            if startIndex < 2:
                continue
            elif startIndex > 2:
                break

            softirq_resp.append(line) 

        if len(softirq_resp) <= 1:
            return softirq_data

        softirq_resp.pop(0)
        softirq_resp.pop(0)
        for line in softirq_resp:
            line_values = line.split()

            softirq_stat = {}
            try:
                softirq_stat['HRTIMER'] = self.client.toDecimal(line_values[-2])
                softirq_stat['TASKLET'] = self.client.toDecimal(line_values[-4])
                softirq_stat['NET_RX'] = self.client.toDecimal(line_values[-7])
                softirq_stat['NET_TX'] = self.client.toDecimal(line_values[-8])

                cpu_name = line_values[1]
            except Exception as err:
                print(err)
                continue

            softirq_data['data'][cpu_name] = softirq_stat

        return softirq_data


    # def get_stat(self, response_lines=[]):

    #     if not response_lines:
    #         response_lines = self.client.getResponse('GetCmdMpstat')
    #     elif isinstance(response_lines, str):
    #         response_lines = self.client.split_to_lines(response_lines)


    #     # discard the first two lines
    #     response_lines.pop(0)
    #     response_lines.pop(0)

    #     if not response_lines:
    #         return None
    #         response_lines.pop(0)

    #     # Basic data, basically for debugging
    #     stat_data = {
    #         "lepd_command": "GetCmdMpstat",
    #         "rawResult": response_lines,
    #         "server": self.server
    #     }

    #     # this is for analysis
    #     irq_numbers = []
    #     softirq_numbers = []

    #     # Core data, for displaying
    #     stat_data['data'] = {}
    #     stat_data['data']['cpu_stat'] = {}
    #     for line in response_lines:
            
    #         if (line.strip() == ''):
    #             break
            
    #         line_values = line.split()

    #         cpu_stat = {}
    #         try:
    #             cpu_stat['idle'] = float(line_values[-1])
    #             cpu_stat['gnice'] = float(line_values[-2])
    #             cpu_stat['guest'] = float(line_values[-3])
    #             cpu_stat['steal'] = float(line_values[-4])
    #             cpu_stat['soft'] = float(line_values[-5])
    #             cpu_stat['irq'] = float(line_values[-6])
    #             cpu_stat['iowait'] = float(line_values[-7])
    #             cpu_stat['system'] = float(line_values[-8])
    #             cpu_stat['nice'] = float(line_values[-9])
    #             cpu_stat['user'] = float(line_values[-10])

    #             cpu_name = line_values[-11]
    #         except Exception as err:
    #             print(err)
    #             continue

    #         # this is for mocking data
    #         # current_minute = datetime.now().minute
    #         # if current_minute % 2 == 0:
    #         #     if cpu_name == '0':
    #         #         cpu_stat['irq'] = Decimal(80)
    #         #     else:
    #         #         cpu_stat['irq'] = Decimal(20)



    #         stat_data['data']['cpu_stat'][cpu_name] = cpu_stat

    #     # analysis for load balance
    #     analysis_report = self.analyze_irq_for_load_balance(stat_data['data']['cpu_stat'])
    #     if analysis_report:
    #         if 'messages' not in stat_data:
    #             stat_data['messages'] = []

    #         analysis_report['source'] = 'irq'
    #         stat_data['messages'].append(analysis_report)

    #     #get irq info from stat_data
    #     irq_info = self.get_irq(response_lines)
    #     if (irq_info != None):
    #         stat_data['data']['irq'] = irq_info['data']

    #     #get soft irq info from stat_data
    #     softirq_info = self.get_soft_irq(response_lines)
    #     if (softirq_info != None):
    #         stat_data['data']['softirq'] = softirq_info['data']

    #     return stat_data


    def analyze_irq_for_load_balance(self, cpu_stat_data):

        if not cpu_stat_data:
            return None

        if len(cpu_stat_data) < 2:
            return None

        irq_list = []
        for core_name in cpu_stat_data:
            if core_name == 'all':
                continue
            irq_list.append(cpu_stat_data[core_name])

        # TODO: will refactor in the future, the logic below is just for demo
        # a very simple logic: if any two irq values has a difference of over 30% variance, we say it's not load balanced.
        for index, item in enumerate(irq_list):
            if index == len(irq_list) - 1:
                break

            irqValue = item['irq'] + item['soft']
            nextIrqValue = irq_list[index+1]['irq'] + irq_list[index+1]['soft']

            variance = abs(irqValue - nextIrqValue)
            # print("variance: " + str(variance))
            if variance >= self.loadBalanceBenchMark:
            # if randrange(10) > 4:   # this is just for mocking
                print("IRQ variance=" + str(variance) + ">=0.4, load NOT balanced")
                return {
                    'level': "warning",
                    "message": "Load NOT balanced! ",
                    "time": strftime("%Y-%m-%d %H:%M:%S", gmtime())
                }
            # else:
                # print("IRQ variance less than 0.3, load balanced")

        return None


    def get_average_load(self, response_lines = None):

        lepd_command = 'GetProcLoadavg'
        if not response_lines:
            response_lines = self.client.getResponse(lepd_command)
        elif isinstance(response_lines, str):
            response_lines = self.client.split_to_lines(response_lines)

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

        lepd_command = 'GetCmdTop'
        if (responseLines == None):
            responseLines = self.client.getResponse(lepd_command)

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

    now = gmtime()

    pp = pprint.PrettyPrinter(indent=2)
    
    profiler = CPUProfiler('www.rmlink.cn')

    # pp.pprint(profiler.get_softirq())

    pp.pprint(profiler.get_irq())
    # pp.pprint(profiler.getIrqInfo())
    # pp.pprint(profiler.getSoftIrqInfo())
    # pp.pprint(profiler.getCapacity())
    # pp.pprint(profiler.getProcessorCount())
    pp.pprint(profiler.get_status())
    # pp.pprint(profiler.getAverageLoad())
    # pp.pprint(profiler.getTopOutput())
    # pp.pprint(profiler.getCpuByName("kworker/u3:0"))
    # pp.pprint(profiler.getCpuByPid("4175"))
    # pp.pprint(profiler.getTopHResult())

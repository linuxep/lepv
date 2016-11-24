"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import json
import socket
from decimal import Decimal
import pprint
import re

class LepDClient:

    def __init__(self, server, port=12307):
        self.server = server
        self.port = port
        self.bufferSize = 2048
        self.debug = False

    def listAllMethods(self):
        response = self.sendRequest("ListAllMethod")
        if (response == None or 'result' not in response):
            return None
        
        results = response['result'].strip().split(" ")
        return results

    def ping(self):
        response = self.sendRequest("SayHello")
        print("response from SayHello: ")
        
        if (self.debug):
            print("Ping in debug mode")
        else:
            print("Ping in release mode")
            
        print(response)
        if (response != None and 'result' in response and response['result'].startswith('Hello')):
            return True
        else:
            return False
        
    def getIOStat(self):
        response = self.sendRequest("GetCmdIostat")
        if (response == None or 'result' not in response):
            return None
        
        # TODO
        # seems like IOStat command needs to run with "x" option according to Barry's document, will wait for Bob's update before moving on.
        results = response['result'].strip().split("\n")
        # for line in results:
        #     print(line)
            
        return results

    def getSMem(self):
        response = self.sendRequest("GetCmdSmem")
        if (response == None or 'result' not in response):
            return None

        results = response['result'].strip().split("\n")
        return results

    def getProcRank(self):
        # TODO: returns empty JSON,  @Bob please take a look
        response = self.sendRequest("GetCmdProcrank")
        if (response == None or 'result' not in response):
            return None

        results = response['result'].strip().split("\n")
        # for line in results:
        #     print(line)

        return results

    def getAverageLoad(self):
        response = self.sendRequest("GetProcLoadavg")
        if (response == None or 'result' not in response):
            return None
        
        results = response['result'].strip().split(" ")
        return results

    def getProcMeminfo(self):
        response = self.sendRequest("GetProcMeminfo")
        if (response == None or 'result' not in response):
            return None

        results = {}
        result = response['result'].strip()
        lines = result.split("\n")
        for line in lines:
            linePairs = line.split(":")
            lineKey = linePairs[0].strip()
            lineValue = linePairs[1].replace('kB', '').strip()

            results[lineKey] = lineValue

        return results
    
    

    def getProcCpuinfoX(self):
        
        responseARM = '{"result":	"Processor\\t: ARMv7 Processor rev 4 (v7l)\\nprocessor\\t: 0\\nBogoMIPS\\t: 1810.43\\n\\nprocessor\\t: 1\\nBogoMIPS\\t: 1823.53\\n\\nFeatures\\t: swp half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt \\nCPU implementer\\t: 0x41\\nCPU architecture: 7\\nCPU variant\\t: 0x0\\nCPU part\\t: 0xc07\\nCPU revision\\t: 4\\n\\nHardware\\t: sun7i\\nRevision\\t: 0000\\nSerial\\t\\t: 0000000000000000\\nlepdendstring"}'
        
        responseX86 = '{"result":	"processor\\t: 0\\nvendor_id\\t: GenuineIntel\\ncpu family\\t: 6\\nmodel\\t\\t: 6\\nmodel name\\t: QEMU Virtual CPU\\nstepping\\t: 3\\nmicrocode\\t: 0x1\\ncpu MHz\\t\\t: 2599.998\\ncache size\\t: 4096 KB\\nphysical id\\t: 0\\nsiblings\\t: 1\\ncore id\\t\\t: 0\\ncpu cores\\t: 1\\napicid\\t\\t: 0\\ninitial apicid\\t: 0\\nfpu\\t\\t: yes\\nfpu_exception\\t: yes\\ncpuid level\\t: 13\\nwp\\t\\t: yes\\nflags\\t\\t: fpu de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pse36 clflush mmx fxsr sse sse2 syscall nx lm rep_good nopl pni cx16 x2apic popcnt hypervisor lahf_lm\\nbugs\\t\\t:\\nbogomips\\t: 5199.99\\nclflush size\\t: 64\\ncache_alignment\\t: 64\\naddress sizes\\t: 40 bits physical, 48 bits virtual\\npower management:\\n\\nprocessor\\t: 1\\nvendor_id\\t: GenuineIntel\\ncpu family\\t: 6\\nmodel\\t\\t: 6\\nmodel name\\t: QEMU Virtual CPU\\nstepping\\t: 3\\nmicrocode\\t: 0x1\\ncpu MHz\\t\\t: 2599.998\\ncache size\\t: 4096 KB\\nphysical id\\t: 1\\nsiblings\\t: 1\\ncore id\\t\\t: 0\\ncpu cores\\t: 1\\napicid\\t\\t: 1\\ninitial apicid\\t: 1\\nfpu\\t\\t: yes\\nfpu_exception\\t: yes\\ncpuid level\\t: 13\\nwp\\t\\t: yes\\nflags\\t\\t: fpu de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pse36 clflush mmx fxsr sse sse2 syscall nx lm rep_good nopl pni cx16 x2apic popcnt hypervisor lahf_lm\\nbugs\\t\\t:\\nbogomips\\t: 5199.99\\nclflush size\\t: 64\\ncache_alignment\\t: 64\\naddress sizes\\t: 40 bits physical, 48 bits virtual\\npower management:\\n\\nlepdendstring"}'
        
        response = json.loads(responseARM)
        
        return response

    def getProcCpuinfo(self):
        response = self.sendRequest("GetProcCpuinfo")
        if (response == None or 'result' not in response):
            return None

        return response['result'].strip()
        
        return result

    def getTopOutput(self):
        response = self.sendRequest("GetCmdTop")
        if (response == None or 'result' not in response):
             return None

        response = response['result'].strip().split("\n")
        
        headerLine = response.pop(0)
        # print(headerLine)
        # if (headerLine != 'PID USER     PRI  NI    VSZ   RSS S %CPU %MEM     TIME CMD'):
        #     print("Header line changed, pay attention")
        
        result = {}
        for responseLine in response:
            # print(responseLine)
            lineValues = responseLine.split()
            
            pid = lineValues[0]
            result[pid] = {}

            result[pid]['pid'] = pid
            result[pid]['user'] = lineValues[1]
            result[pid]['pri'] = lineValues[2]
            result[pid]['ni'] = lineValues[3]
            result[pid]['vsz'] = lineValues[4]
            result[pid]['rss'] = lineValues[5]
            result[pid]['s'] = lineValues[6]
            result[pid]['cpu'] = lineValues[7]
            result[pid]['mem'] = lineValues[8]
            result[pid]['time'] = lineValues[9]

            result[pid]['command'] = ' '.join([str(x) for x in lineValues[10:]])
            
            if(len(result) >= 25):
                break

        return result

    def getTopHOutput(self):
        response = self.sendRequest("GetCmdTopH")
        if (response == None or 'result' not in response):
             return None

        results = {}
        results = response['result'].strip()
        results = results.split("\n")
        return results

    def getSmemOutput(self):
        response = self.sendRequest("GetCmdSmem")
        if (response == None or 'result' not in response):
             return None

        results = {}
        results = response['result'].strip()
        results = results.split("\n")
        return results

    def getProcrankOutput(self):
        response = self.sendRequest("GetCmdProcrank")
        if (response == None or 'result' not in response):
             return None

        results = {}
        results = response['result'].strip()
        results = results.split("\n")
        return results
    
    def getCmdDf(self):
        response = self.sendRequest("GetCmdDf")
        if (response == None or 'result' not in response):
            return None

        results = response['result'].strip()

        resultLines = results.split('\n')

        diskData = {}
        for resultLine in resultLines:
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

        return diskData

    def getCmdVmstat(self):
        response = self.sendRequest("GetCmdVmstat")
        if (response == None or 'result' not in response):
            return None

        results = response['result'].strip()
        # TODO: need to parse it to structured data.
        return results

    def getCmdPerfFaults(self):
        response = self.sendRequest("GetCmdPerfFaults")
        if (response == None or 'result' not in response):
            return None

        results = response['result'].strip().split('\n')
        return results

    def getCmdPerfCpuclock(self, count=25):
        response = self.sendRequest("GetCmdPerfCpuclock")
        if (response == None or 'result' not in response):
            return None

        results = response['result'].strip().split('\n')
        resultList = []
        for line in results:
            if (line.strip() == ''):
                continue
                
            # print(line)
            lineValues = line.split()
            
            if (len(lineValues) < 5):
                # print('                     --------------- skip it.')
                continue

            if ('%' not in lineValues[0]):
                # print('                     --------------- skip it.')
                continue
                
            resultLine = {}
            resultLine['Overhead'] = lineValues[0]
            resultLine["Command"] = lineValues[1]
            resultLine["Shared Object"] = lineValues[2]
            resultLine['Symbol'] = ' '.join([str(x) for x in lineValues[3:]])
            
            resultList.append(resultLine)
            if (len(resultList) >= count):
                # print('now the length of the array is greater than the max, break here')
                break

        return {'result': resultList}

    def getIostatResult(self):
        response = self.sendRequest("GetCmdIostat")
        if (response == None or 'result' not in response):
            return None

        resultLines = response['result'].split('\n')
        # 'Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util'
        # 'vda               9.31     0.44    0.24    0.42    38.76     4.04   129.68     0.00 6331.59 14163.45 1931.28   1.58   0.10'

        for i in range(len(resultLines)):
            if (not resultLines[i].startswith('Device:')):
                continue
            
            return resultLines[i:]

        # headerLine = resultLines[2]
        # valueLine = resultLines[3]
        # headers = headerLine.split()
        # values = valueLine.split()
        # 
        # resultMap = {}
        # index = 0
        # while(index < len(headers)):
        #     header = headers[index].replace("/s", "").replace(":", "").replace("%", "")
        #     value = values[index]
        # 
        #     resultMap[header] = value
        #     
        #     index = index + 1
        # 
        # return resultMap

    def getCmdMpStat(self):
        response = self.sendRequest("GetCmdMpstat")
        if (response == None or 'result' not in response):
            return None

        lines = response['result'].strip().split("\n")

        lines.pop(0)
        lines.pop(0)
        return lines

        # for line in lines:
        #     lineValues = line.split()
        #     for lineValue in lineValues:
        #         print(lineValue)


    def getProcStat(self):
        response = self.sendRequest("GetProcStat")
        if (response == None or 'result' not in response):
            return None

        procStats = {}
        lines = response['result'].strip().split("\n")
        for line in lines:
            if "cpu" in line:
                data = line.split(" ")
                if data[1] == "":
                    data.pop(1)
                #This is cpuX
                procStat = {}

                procStat['id'] = data[0]
                procStat['user'] = Decimal(data[1])
                procStat['nice'] = Decimal(data[2])
                procStat['system'] = Decimal(data[3])
                procStat['idle'] = Decimal(data[4])
                procStat['iowait'] = Decimal(data[5])
                procStat['irq'] = Decimal(data[6])
                procStat['softirq'] = Decimal(data[7])
                procStat['steal'] = Decimal(data[8])
                procStat['guest'] = Decimal(data[9])
                procStat['guestnice'] = Decimal(data[10])

                total = procStat['user'] + procStat['nice'] + procStat['system'] + procStat['idle'] + procStat['iowait'] + procStat['irq'] + procStat['softirq'] + procStat['steal'] + procStat['guest'] + procStat['guestnice']

                procStat['user.ratio'] = Decimal(procStat['user'] / total * 100).quantize(Decimal('0.00'))
                procStat['nice.ratio'] = Decimal(procStat['nice'] / total * 100).quantize(Decimal('0.00'))
                procStat['system.ratio'] = Decimal(procStat['system'] / total * 100).quantize(Decimal('0.00'))
                procStat['idle.ratio'] = Decimal(procStat['idle'] / total * 100).quantize(Decimal('0.00'))
                procStat['iowait.ratio'] = Decimal(procStat['iowait'] / total * 100).quantize(Decimal('0.00'))
                procStat['irq.ratio'] = Decimal(procStat['irq'] / total * 100).quantize(Decimal('0.00'))
                procStat['softirq.ratio'] = Decimal(procStat['softirq'] / total * 100).quantize(Decimal('0.00'))
                procStat['steal.ratio'] = Decimal(procStat['steal'] / total * 100).quantize(Decimal('0.00'))
                procStat['guest.ratio'] = Decimal(procStat['guest'] / total * 100).quantize(Decimal('0.00'))
                procStat['guestnice.ratio'] = Decimal(procStat['guestnice'] / total * 100).quantize(Decimal('0.00'))

                procStats[procStat['id']] = procStat

        return procStats

    def getIoTop(self):
        response = self.sendRequest("GetCmdIotop")
        if (response == None or 'result' not in response):
            return None
    
        lines = response['result'].strip().split("\n")
        return lines
    
    
    def tryAllMethods(self):
        methods = self.listAllMethods()
        
        failedMethods = []
        for methodName in methods:
            print('')
            print('<[ ' + methodName + " ]>")
            response = self.sendRequest(methodName)

            if (response == None or 'result' not in response):
                failedMethods.append(methodName)
                continue

            lines = response['result'].strip().split("\n")
            for line in lines:
                print(line)

        if (len(failedMethods) > 0):
            print("Methods that returned empty response:")
            for methodName in failedMethods:
                print(methodName)
        else:
            print("\n\nAdd methods are working!")

    def sendRequest(self, methodName):
        sock = None

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialise our socket
            sock.connect((self.server, self.port)) # connect to host <HOST> to port <PORT>

            input_data = {}
            input_data['method'] = methodName

            dumped_data = json.dumps(input_data) # Dump the input dictionary to proper json

            sock.send(dumped_data.encode())
            serverResponse = str.encode("")
            end = str.encode("lepdendstring")
            while True:
                data = sock.recv(self.bufferSize)
                if end in data:
                    data = data.replace(end,str.encode(""))
                    serverResponse = serverResponse + data
                    break
                serverResponse = serverResponse + data
            responseJsonDecoded = json.loads(serverResponse.decode()) # decode the data received

            return responseJsonDecoded

        except Exception as error:
            print(methodName + ": " + str(error))
        finally:
            if (sock):
                sock.close()

if( __name__ =='__main__' ):

    pp = pprint.PrettyPrinter(indent=2)
    client = LepDClient('www.linuxxueyuan.com')
    
    client.getProcCpuinfoX()

    # client = LepDClient('www.linuxxueyuan.com')

    # client.getCmdPerfCpuclock()
    
    # client.tryAllMethods()

    # pp.pprint(client.getIoTop())
    # pp.pprint(client.getCmdMpStat())
    
    # pp.pprint(client.sendRequest('GetProcSlabinfo'))
    # 
    # pp.pprint(client.ping())
    # 
    # print(client.getCmdVmstat())
    # 
    # pp.pprint(client.getAverageLoad())
    # 
    # pp.pprint(client.getTopResult())




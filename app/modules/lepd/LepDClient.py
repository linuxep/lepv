"""Core module for interacting with LEPD"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import json
import socket
from decimal import Decimal
import pprint
import re
import datetime

class LepDClient:

    def __init__(self, server, port=12307, config='release'):
        self.server = server
        self.port = port
        self.bufferSize = 2048
        self.config = config
        
        self.LEPDENDINGSTRING = 'lepdendstring'

    def listAllMethods(self):
        response = self.sendRequest('ListAllMethod')
        if (response == None or 'result' not in response):
            return []

        lines = response['result'].strip().split()
        return lines

    def ping(self):
        # print('Send "SayHello" command to LEPD')
        response = self.sendRequest("SayHello")
            
        # print(response)
        if (response != None and 'result' in response and response['result'].startswith('Hello')):
            return True
        else:
            return False
    
    def toDecimal(self, val, precision='0.00'):
        try:
            return Decimal(val).quantize(Decimal(precision))
        except:
            return 0.00
                                        
        
    def getTopOutput(self):
        response = self.sendRequest("GetCmdTop")
        if (response == None or 'result' not in response):
             return None

        response = response['result'].strip().split("\n")
        
        headerLine = response.pop(0)
        
        result = {}
        for responseLine in response:
            # print(responseLine)
            if (self.LEPDENDINGSTRING in responseLine):
                break

            if(len(result) >= 25):
                break
                
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

        return result

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

    def getCmdMpStat(self):
        response = self.sendRequest("GetCmdMpstat")
        if (response == None or 'result' not in response):
            return None

        lines = response['result'].strip().split("\n")

        lines.pop(0)
        lines.pop(0)
        return lines


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
    
    def tryAllMethods(self):
        methods = self.listAllMethods()
        
        executionResuts = {}
        for methodName in methods:

            print('')
            print('<[ ' + methodName + " ]>")
            
            executionResuts[methodName] = {}

            startTime = datetime.datetime.now()
            response = self.sendRequest(methodName)
            endTime = datetime.datetime.now()
            executionResuts[methodName]['duration'] = "%.1f" % ((endTime - startTime).total_seconds())
            print('duration:=' + executionResuts[methodName]['duration'])
            
            if (response == None or 'result' not in response):
                executionResuts[methodName]['return'] = None
                print('Return:= Failed!')
            else:
                lines = response['result'].strip().split("\n")
                executionResuts[methodName]['return'] = lines
                for line in lines:
                    print(line)
        
        
        print("")
        print("Summary:")

        for methodName, executionResult in executionResuts.items():
            resultSumamry = "[" + methodName + "]("
            if (executionResult['return'] == None):
                resultSumamry += "Failed) in " 
            else:
                resultSumamry += "Succeeded) in "
            
            resultSumamry += executionResult['duration'] + ' seconds'
            print(resultSumamry)
        
        return executionResuts

    def getUnitTestResponse(self, commandName, arch='arm'):
        
        currentDir = os.path.dirname(os.path.realpath(__file__))
        jsonFilePath = os.path.join(currentDir, 'tests', commandName, 'raw', arch + ".txt")
        
        with open(jsonFilePath) as data_file:
            return json.load(data_file)
    
    def getSystemInfo(self):
        responseLines = self.getResponse('GetProcVersion')
        if (len(responseLines) == 0):
            return {}
        
        # it has just one line
        # a line like this:
        # Linux version 3.13.0-86-generic (buildd@lgw01-19) (gcc version 4.8.2 (Ubuntu 4.8.2-19ubuntu1) ) #130-Ubuntu SMP Mon Apr 18 18:27:15 UTC 2016
        responseLine = responseLines.pop(0)
        
        sysInfo = {}
        sysInfo['os'] = 'linux'
        sysInfo['kernel'] = '3.13.0-86-generic'
        sysInfo['gcc'] = '4.8.2'
        sysInfo['distribution'] = 'ubuntu'
        sysInfo['version'] = '4.8.2'
        
        return sysInfo
        
    
    def getResponse(self, methodName):
        if (self.config != 'unittest'):
            response = self.sendRequest(methodName)
        else:
            response = self.getUnitTestResponse(methodName)
            
        if (response == None or 'result' not in response):
            return []

        lines = re.split(r'\\n|\n', response['result'].strip())
        return lines
        
        
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
            pass
            # print(methodName + ": " + str(error))
            # if (error.strerror == 'nodename nor servname provided, or not known'):
            #     print('please double check the server to monitor is reachable, and the method is supported by LEPD')
        finally:
            if (sock):
                sock.close()

if( __name__ =='__main__' ):
    
    # MEMO:
    # procrank is to replace smem, ( smem will retire )
    # iopp is to replace iotop, ( iotop is to retire )
    # df is now supported

    pp = pprint.PrettyPrinter(indent=2)
    client = LepDClient('www.rmlink.cn', config='debug')
    
    # pp.pprint(client.getSystemInfo())
    pp.pprint(client.listAllMethods())
    # pp.pprint(client.getResponse('GetCmdDf'))


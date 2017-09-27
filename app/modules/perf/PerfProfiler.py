"""Module for Perf related data parsing"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import pprint

from modules.lepd.LepDClient import LepDClient

__author__ = 'xmac'

class PerfProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        self.client = LepDClient(self.server)
        self.config = config
        
        self.dataCount = 25

    def getPerfCpuClock(self):

        responseLines = self.client.getResponse("GetCmdPerfCpuclock")
        if (len(responseLines) == 0):
            return {}

        responseData = {}
        if (self.config == 'debug'):
            responseData['rawResult'] = responseLines[:]
        
        columnHeaderLinePrefix = '# Overhead'
        while( not responseLines[0].startswith(columnHeaderLinePrefix)):
            responseLines.pop(0)
        
        responseLines.pop(0)
        responseLines.pop(0)
        responseLines.pop(0)

        resultList = []
        for line in responseLines:
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
            if (len(resultList) >= self.dataCount):
                # print('now the length of the array is greater than the max, break here')
                break

        responseData['data'] = resultList
        return responseData

if( __name__ =='__main__' ):
    profiler = PerfProfiler(server='www.readeeper.com', config='debug')

    pp = pprint.PrettyPrinter(indent=2)
    
    responseData = profiler.getPerfCpuClock()
    pp.pprint(responseData)


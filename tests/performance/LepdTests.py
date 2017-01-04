"""Tests for LEPV"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from tests.unittests.LepDRequestor import LepDRequestor
from backend.LepDClient import LepDClient
from datetime import datetime

__author__ = 'xmac'

class LepDTests():

    def __init__(self, server):
        self.server = server
    
    def runMethodConcurrently(self, command, times):
        
        # print("Testing command '" + command + "' with " + str(times) + " threads concurrently.")
        processes = []
        
        while times > 0:
            lepdRequestor = LepDRequestor(command, self.server)
            processes.append(lepdRequestor)
            lepdRequestor.start()
            
            times = times - 1

        for process in processes:
            process.join()

        for process in processes:
            process.report()
    
    def checkAndReportThreads(self, lepdRequestors):
        if (len(lepdRequestors) == 0):
            return
        
        requestsCompleted = []
        for lepdRequest in lepdRequestors:
            if (not lepdRequest.isAlive()):
                requestsCompleted.append(lepdRequest)
                lepdRequest.report()
            
            lepdRequest.join()
        
        for lepdRequest in requestsCompleted:
            lepdRequestors.remove(lepdRequest)
        
        if (len(lepdRequestors) > 0):
            self.checkAndReportThreads(lepdRequestors)
        

    def runAllMethodsConcurrently(self):

        # print("Running all commands concurrently...\n")
        processes = []

        client = LepDClient(self.server)
        commands = client.listAllMethods()

        timeStarts = datetime.utcnow().replace()

        for command in commands:
            # print(command)

            lepdRequestor = LepDRequestor(command, self.server)
            processes.append(lepdRequestor)
            lepdRequestor.start()
        
        # print('\nRunning and checking status...\n')
        self.checkAndReportThreads(processes)

        timeEnds = datetime.utcnow().replace()
        duration = timeEnds - timeStarts

        durationInSeconds = duration.seconds + duration.microseconds / 1000000
        timeUsed = "{:.3f}".format(durationInSeconds)
        
        print("\nAll done in " + timeUsed + " Seconds\n")

    def runMethodRepeatedly(self, command, times):
        print("Testing command '" + command + "' for " + str(times) + " times.")
        i = 1
        while i <= times:
            print("")
            print(i)
            
            lepdRequestor = LepDRequestor(command, self.server)
            lepdRequestor.start()
            lepdRequestor.join()
            lepdRequestor.report()

            i = i + 1
    
    
    def runAllMethodsRepeatedly(self):
        client = LepDClient(self.server)
        commands = client.listAllMethods()

        for command in commands:
            print("Running command: " + command)
            
            i = 1
            while( i <= 3 ):
                self.runMethodConcurrently(command, 1)
                i += 1


if( __name__ =='__main__' ):
    
    server = 'www.linuxep.com'
    print("Testing against: " + server)
    
    tests = LepDTests(server)
    # tests.runAllMethodsRepeatedly()

    tests.runAllMethodsConcurrently()
        
    
    # tests.runMethodConcurrently("GetCmdPerfCpuclock", 2)
    # tests.runMethodRepeatedly("GetCmdPerfCpuclock", 20)






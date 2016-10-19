"""Tests for LEPV"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from backend.LepDRequestor import LepDRequestor

__author__ = 'xmac'

class LepDTests:

    def __init__(self, server):
        self.server = server
    
    def runMethodConcurrently(self, command, times):
        
        processes = []
        
        while times > 0:
            lepdRequestor = LepDRequestor(command)
            processes.append(lepdRequestor)
            lepdRequestor.start()
            
            times = times - 1

        for process in processes:
            process.join()

        for process in processes:
            process.report()

    def runMethodRepeatedly(self, command, times):

        i = 1
        while i <= times:
            print("")
            print(i)
            
            lepdRequestor = LepDRequestor(command)
            lepdRequestor.start()
            lepdRequestor.join()
            lepdRequestor.report()

            i = i + 1


if( __name__ =='__main__' ):
    
    tests = LepDTests('www.linuxep.com')
    tests = LepDTests('www.linuxxueyuan.com')
    tests.runMethodConcurrently("GetCmdIostat", 10)
    tests.runMethodRepeatedly("GetCmdIostat", 20)






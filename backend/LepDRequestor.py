"""core utility module for JSON RPC requests"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from backend.LepDClient import LepDClient
import threading
from datetime import datetime

__author__ = 'xmac'

class LepDRequestor(threading.Thread):

    def __init__(self, lepdCommand, server='www.linuxep.com', port=12307):
        threading.Thread.__init__(self)
        
        self.timeUsed = 0
        
        self.command = lepdCommand
        self.lepDClient = LepDClient(server, port)
        
        self.response = ''


    def run(self):
        timeStarts = datetime.utcnow().replace()
        
        self.response = self.lepDClient.sendRequest(self.command)
    
        timeEnds = datetime.utcnow().replace()
        duration = timeEnds - timeStarts
        self.timeUsed = int(duration.total_seconds())
    
    
    def report(self):
        print("")
        print("Command: " + self.command)
        print("Duration: " + str(self.timeUsed) + " seconds")
        # print("Result:")
        # print(self.response)
        
    
    def runAndReport(self):
        self.run()
        self.report()
        


if( __name__ =='__main__' ):
    requestor = LepDRequestor('GetCmdIostat')
    
    requestor.runAndReport()
    
    


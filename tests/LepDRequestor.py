"""core utility module for JSON RPC requests"""
__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from backend.LepDClient import LepDClient
import threading
from datetime import datetime

__author__ = 'xmac'

class LepDRequestor(threading.Thread):

    def __init__(self, lepdCommand, server, port=12307):
        threading.Thread.__init__(self, name=lepdCommand)
        
        self.timeUsed = 0
        self.succeeded = False
        
        self.command = lepdCommand
        self.lepDClient = LepDClient(server, port)
        
        self.response = ''


    def run(self):
        timeStarts = datetime.utcnow().replace()
        
        self.response = self.lepDClient.sendRequest(self.command)
        if ("{'result': 'Hello!'}" != self.response):
            self.succeeded = True
    
        timeEnds = datetime.utcnow().replace()
        duration = timeEnds - timeStarts
        
        durationInSeconds = duration.seconds + duration.microseconds / 1000000
        self.timeUsed = "{:.3f}".format(durationInSeconds)

    
    def report(self):
        
        reportMessage = self.command
        # assume the longest command name is of 30 chars
        maxLength = 30
        reportMessage += ' ' * (maxLength - len(self.command)) + ' '
        
        if (self.succeeded):
            reportMessage += "succeeded in "
        else:
            reportMessage += "failed in "
        
        reportMessage += str(self.timeUsed) + " seconds"
        
        print(reportMessage)
        # print("Command: " + self.command)
        # if (self.succeeded):
        #     print("Status: Succeeded")
        # else:
        #     print("Status: Failed!!!")
        #     print(self.response)
        #     
        # print("Duration: " + str(self.timeUsed) + " seconds")
        
    
    def runAndReport(self):
        self.run()
        self.report()
        


if( __name__ =='__main__' ):
    requestor = LepDRequestor('GetCmdIostat', 'www.linuxep.com')
    
    requestor.runAndReport()
    
    


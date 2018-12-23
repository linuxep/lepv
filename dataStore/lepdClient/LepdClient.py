"""Core module for interacting with LEPD"""

__author__ = "Copyright (c) 2016, 李旭升 <programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import json
import pprint
import socket

'''
LepdClient pulls data from lepd 
'''


class LepdClient(object):
    def __init__(self, server, port=12307, config='release'):
        self.server = server
        self.port = port
        self.bufferSize = 2048
        self.config = config

        self.LEPDENDINGSTRING = 'lepdendstring'

    def sendRequest(self, methodName):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server, self.port))

            input_data = {}
            input_data['method'] = methodName

            dumped_data = json.dumps(input_data)

            sock.send(dumped_data.encode())
            serverResponse = str.encode("")
            end = str.encode("lepdendstring")
            while True:
                data = sock.recv(self.bufferSize)
                if end in data:
                    data = data.replace(end, str.encode(""))
                    serverResponse = serverResponse + data
                    break
                serverResponse = serverResponse + data
            responseJsonDecoded = json.loads(serverResponse.decode())
            return responseJsonDecoded
        except Exception as error:
            print("dataStore/lepdClient/LepdClient.py.sendRequest() throws an exception\n")
            pass
        finally:
            if (sock):
                sock.close()

    def listAllMethods(self):
        response = self.sendRequest('ListAllMethod')
        if (response == None or 'result' not in response):
            return []
        lines = response['result'].strip().split()
        return lines


if (__name__ == '__main__'):
    pp = pprint.PrettyPrinter(indent=2)
    client = LepdClient('www.rmlink.cn', config='debug')

    print(client.listAllMethods())

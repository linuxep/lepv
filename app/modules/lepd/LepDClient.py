import click
import datetime
import re
import pprint
import socket
import json
"""Core module for interacting with LEPD"""
__author__ = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."


class LepDClient:

    def __init__(self, server, port=12307, config='release'):
        self.server = server
        self.port = port
        self.bufferSize = 2048
        self.config = config
        self.sock = None

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

    # TODO:
    # Decimal is not a data type supported by JSON
    def toDecimal(self, val, precision='0.00'):
        try:
            return float(val)  # Decimal(val).quantize(Decimal(precision))
        except Exception as err:
            print(err)
            return float(0)

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

    def tryAllMethods(self):
        methods = self.listAllMethods()

        executionResults = {}
        for methodName in methods:

            print('')
            print('<[ ' + methodName + " ]>")

            executionResults[methodName] = {}

            startTime = datetime.datetime.now()
            response = self.sendRequest(methodName)
            endTime = datetime.datetime.now()
            executionResults[methodName]['duration'] = "%.1f" % ((endTime - startTime).total_seconds())
            print('duration:=' + executionResults[methodName]['duration'])

            if (response == None or 'result' not in response):
                executionResults[methodName]['return'] = None
                print('Return:= Failed!')
            else:
                lines = response['result'].strip().split("\n")
                executionResults[methodName]['return'] = lines
                for line in lines:
                    print(line)

        print("")
        print("Summary:")

        for methodName, executionResult in executionResults.items():
            resultSumamry = "[" + methodName + "]("
            if (executionResult['return'] == None):
                resultSumamry += "Failed) in "
            else:
                resultSumamry += "Succeeded) in "

            resultSumamry += executionResult['duration'] + ' seconds'
            print(resultSumamry)

        return executionResults

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

        lines = self.split_to_lines(response['result'])
        return lines

    def split_to_lines(self, longString):
        return re.split(r'\\n|\n', longString.strip())

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initialise our socket
        try:
            sock.connect((self.server, self.port))  # connect to host <HOST> to port <PORT>
        except Exception as e:
            print("conncet error: ", e)
            return None
        self.sock = sock

    def sendRequest(self, methodName):
        while(self.sock is None):
            self.connect()

        sock = self.sock
        try:
            input_data = {}
            input_data['method'] = methodName

            dumped_data = json.dumps(input_data)  # Dump the input dictionary to proper json

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
            responseJsonDecoded = json.loads(serverResponse.decode())  # decode the data received

            return responseJsonDecoded
        except socket.error as err:
            print("connect lost ", err, "  try reconnect")
            self.sock = None
            self.sendRequest(methodName)
            # print(methodName + ": " + str(error))
            # if (error.strerror == 'nodename nor servname provided, or not known'):
            #     print('please double check the server to monitor is reachable, and the method is supported by LEPD')


@click.command()
@click.option('--server', default='www.rmlink.cn', help='Lepd server')
@click.option('--method', default='listAllMethods', help='LepDClient method')
@click.option('--config', default='debug', help='config setting')
@click.option('--out', default=None, help='Log output file')
def main(server, method, config, out):

    # MEMO:
    # procrank is to replace smem, ( smem will retire )
    # iopp is to replace iotop, ( iotop is to retire )
    # df is now supported

    pp = pprint.PrettyPrinter(indent=2)
    client = LepDClient(server, config=config)

    # pp.pprint(client.getSystemInfo())
    func = getattr(client, method)
    results = func()
    if out:
        fp = open(out, 'a')
        fp.write(json.dumps(results))
        fp.write('\n')
        fp.flush()
        fp.close()
    pp.pprint(results)
    # pp.pprint(client.getResponse('GetCmdDf'))


if(__name__ == '__main__'):
    main()
    sys.exit(0)

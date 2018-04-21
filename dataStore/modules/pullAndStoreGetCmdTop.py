__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from app.modules.lepd.LepDClient  import LepDClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetCmdTop from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetCmdTop(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetCmdTop')
    print(res)



if (__name__ == '__main__'):
    lepdClient = LepDClient('www.rmlink.cn')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetCmdTop(lepdClient, influxDbClient)
        time.sleep(1)

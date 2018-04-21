__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from app.modules.lepd.LepDClient  import LepDClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

import time

'''
fetch data related to  GetProcVersion from lepd by lepdClient and 
store the returned data into the influxDB by influxDBClient.
'''
def pullAndStoreGetProcVersion(lepdClient, influxDbClient):
    res = lepdClient.sendRequest('GetProcVersion')
    print(res)



if (__name__ == '__main__'):
    lepdClient = LepDClient('www.rmlink.cn')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):
        pullAndStoreGetProcVersion(lepdClient, influxDbClient)
        time.sleep(1)

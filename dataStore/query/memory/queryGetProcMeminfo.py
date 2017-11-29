__author__ = "李旭升 <programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."


from dataStore.influxDbUtil.dbUtil import myInfluxDbClient

import time

'''
从InfluxDB中查询memory信息
拼接字段还未完成
'''
def queryGetProcMeminfo(influxDbClient):
    res = influxDbClient.query('select * from GetProcMeminfo limit 1')
    print(res)
    help(res)

    return None

if(__name__=='__main__'):
        influxDbClient = myInfluxDbClient('127.0.0.1')
        queryGetProcMeminfo(influxDbClient)


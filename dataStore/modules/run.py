__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient
from dataStore.modules.io.pullAndStoreGetCmdIotop import pullAndStoreGetCmdIotop
from dataStore.modules.cpu.pullAndStoreGetCmdMpstat import pullAndStoreGetCmdMpstat
from dataStore.modules.memory.pullAndStoreGetProcMeminfo import pullAndStoreGetProcMeminfo

import time


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(60):
        pullAndStoreGetCmdIotop(lepdClient, influxDbClient)
        pullAndStoreGetProcMeminfo(lepdClient,influxDbClient)
        pullAndStoreGetCmdMpstat(lepdClient,influxDbClient)
        time.sleep(1)

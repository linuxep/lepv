__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient
from dataStore.modules.io.pullAndStoreGetCmdIostat import pullAndStoreGetCmdIostat
from dataStore.modules.cpu.pullAndStoreGetCmdMpstat import pullAndStoreGetCmdMpstat
from dataStore.modules.memory.memoryPullAndStore import pullAndStoreGetProcMeminfo

import time


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(60):
        pullAndStoreGetCmdIostat(lepdClient, influxDbClient)
        pullAndStoreGetProcMeminfo(lepdClient,influxDbClient)
        pullAndStoreGetCmdMpstat()
        time.sleep(1)

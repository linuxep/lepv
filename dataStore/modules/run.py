__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient
from dataStore.modules.cpu.pullAndStoreGetCmdMpstat import pullAndStoreGetCmdMpstat
from dataStore.modules.memory.pullAndStoreGetProcMeminfo import pullAndStoreGetProcMeminfo
from dataStore.modules.io.pullAndStoreGetCmdIostat import pullAndStoreGetCmdIostat

import time


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(120):
        pullAndStoreGetCmdIostat(lepdClient,influxDbClient)
        pullAndStoreGetProcMeminfo(lepdClient,influxDbClient)
        pullAndStoreGetCmdMpstat(lepdClient,influxDbClient)
        time.sleep(1)

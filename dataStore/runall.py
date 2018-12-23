__author__ = "<programmerli@foxmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from dataStore.lepdClient.LepdClient import LepdClient
from dataStore.influxDbUtil.dbUtil import MyInfluxDbClient

from dataStore.modules.cpu.pullAndStoreGetCmdMpstat import pullAndStoreGetCmdMpstat
from dataStore.modules.io.pullAndStoreGetCmdIostat import pullAndStoreGetCmdIostat
from dataStore.modules.memory.pullAndStoreGetProcMeminfo import pullAndStoreGetProcMeminfo



from dataStore.modules.others.pullAndStoreGetCmdDf import pullAndStoreGetCmdDf
from dataStore.modules.others.pullAndStoreGetCmdDmesg import pullAndStoreGetCmdDmesg
from dataStore.modules.others.pullAndStoreGetCmdFree import pullAndStoreGetCmdFree
from dataStore.modules.others.pullAndStoreGetCmdIotop import pullAndStoreGetCmdIotop
from dataStore.modules.others.pullAndStoreGetCmdIrqInfo import pullAndStoreGetCmdIrqInfo




import time


if (__name__ == '__main__'):
    lepdClient = LepdClient('localhost')
    influxDbClient = MyInfluxDbClient('localhost')
    for i in range(1):

        pullAndStoreGetCmdIostat(lepdClient,influxDbClient)
        pullAndStoreGetProcMeminfo(lepdClient,influxDbClient)
        pullAndStoreGetCmdMpstat(lepdClient,influxDbClient)


        time.sleep(1)

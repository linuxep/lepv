#!/bin/bash  

# SayHello ListAllMethod GetProcMeminfo GetProcLoadavg GetProcVmstat GetProcZoneinfo GetProcBuddyinfo 
# GetProcCpuinfo GetProcSlabinfo GetProcSwaps GetProcInterrupts GetProcSoftirqs GetProcDiskstats 
# GetProcVersion GetProcStat GetProcModules GetCmdIopp GetCmdFree GetCmdProcrank GetCmdIostat GetCmdTop 
# GetCmdDmesg GetCmdDf GetCmdMpstat GetCmdPerfFaults GetCmdPerfCpuclock


echo "SayHello:"
echo "{\"method\":\"SayHello\"}" | nc localhost 12307

echo ""
echo "GetCmdDf:"
echo "{\"method\":\"GetCmdDf\"}" | nc localhost 12307

echo ""
echo "GetProcMeminfo:"
echo "{\"method\":\"GetProcMeminfo\"}" | nc localhost 12307

echo ""
echo "GetProcLoadavg:"
echo "{\"method\":\"GetProcLoadavg\"}" | nc localhost 12307

echo ""
echo "TODO: need to add all the rest methods for testing"
echo ""
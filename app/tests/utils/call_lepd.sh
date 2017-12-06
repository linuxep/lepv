#!/bin/bash

# echo "{\"method\":\"GetProcMeminfo\"}" | nc localhost 12307

if [ "$#" -ne 2 ] ;then
    echo "WARNING:"
    echo "Two params required, the first is the LEPD command name, the second is the server IP/Name to be monitored."
    echo "[Sample usage]:"
    echo "call_lepd.sh GetProcMeminfo www.rmlink.cn"
    echo ""
    echo "[Supported LEPD commands]:"
    echo "GetProcMeminfo"
    echo "GetProcCpuinfo"
    echo ""
else
    echo "{\"method\":\"$1\"}" | nc $2 12307
fi

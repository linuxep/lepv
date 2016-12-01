#!/bin/bash  

echo "SayHello:"
echo "{\"method\":\"SayHello\"}" | nc localhost 12307

echo ""
echo "GetCmdDf:"
echo "{\"method\":\"GetCmdDf\"}" | nc localhost 12307

echo "nc working"

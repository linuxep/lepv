#!/bin/bash  

echo "running LEPD Ubuntu container:"
docker ps

echo "stop and remove existing LEPD container"
docker ps -a | grep 0.0.0.0:12307 | awk '{print $1}' | xargs -I {} docker stop {} | xargs -I {} docker rm {}

echo "Run LEPD in container"
docker run -t -p 12307:12307 linuxep/lepd
echo "LEPD is now running"
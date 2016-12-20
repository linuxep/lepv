#!/bin/bash  

echo "running container:"
docker ps

echo "stop and remove existing LEPV container"
docker ps -a | grep 0.0.0.0:8889 | awk '{print $1}' | xargs -I {} docker stop {} | xargs -I {} docker rm {}

echo "Run LEPV in container"
docker run -t -p 8889:8889 linuxep/lepv0.1
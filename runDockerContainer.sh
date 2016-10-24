#!/bin/bash  

echo "running container:"
docker ps

echo "stop and remove existing lepv container"
docker ps -a | awk '{ print $1,$2 }' | grep linuxep/lepv0.1 | awk '{print $1 }' | xargs -I {} docker stop {} | xargs -I {} docker rm {}

echo "Run LEPV in container"
docker run -t -p 8889:8889 linuxep/lepv0.1

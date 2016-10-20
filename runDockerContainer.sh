#!/bin/bash  

echo "stop and remove existing lepv container"
docker rm $(docker stop $(docker ps -a -q --filter ancestor=mxu/lepv0.1 --format="{{.ID}}"))

echo "Run LEPV in container"
docker run -t -p 8889:8889 mxu/lepv0.1

#!/bin/bash  

echo "running container:"
docker ps

echo "stop and remove existing LEPV container"

# remove by port
docker ps -a | grep 0.0.0.0:8889 | awk '{print $1}' | xargs -I {} docker stop {} | xargs -I {} docker rm {}

# remove by image name
docker ps -a | grep lepv | awk '{print $1}' | xargs -I {} docker stop {} | xargs -I {} docker rm {}

echo "Run LEPV in container"

os=$( uname )
echo "OS: $os"
if [ "$os" == "Darwin" ]; then
    echo "Running Docker container on MacOS"
    docker run -t -p 8889:8889 linuxep/lepv0.1
else
    echo "Running Docker container on Linux"
    docker run -t --net="host" linuxep/lepv0.1
fi
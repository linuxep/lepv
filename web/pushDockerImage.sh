#! /bin/bash
echo "Building docker image and push to DockerHub as linuxep/lepv"
docker build -f docker/Dockerfile -t linuxep/lepv:latest .
docker login
docker push linuxep/lepv

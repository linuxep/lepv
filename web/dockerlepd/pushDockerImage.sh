#! /bin/bash
echo "Building docker image and push to DockerHub as linuxep/lepd"
docker build -f Dockerfile -t linuxep/lepd:latest .
docker login
docker push linuxep/lepd

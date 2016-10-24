#! /bin/bash
echo "Building docker image"
docker build -f DockerBasic/Dockerfile -t linuxep/lepv0.1 .

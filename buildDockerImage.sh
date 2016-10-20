#! /bin/bash
echo "Building docker image"
docker build -f DockerBasic/Dockerfile -t mxu/lepv0.1 .

#! /bin/bash
echo "Building docker image"
docker build -f docker/Dockerfile -t linuxep/lepv0.1 .

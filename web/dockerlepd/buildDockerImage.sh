#! /bin/bash
echo "Building LEPD Ubuntu docker image"
docker build -f Dockerfile -t linuxep/lepd .

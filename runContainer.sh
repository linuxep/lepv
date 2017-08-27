#!/bin/bash  

#####  APP specific variables  #######
DOCKER_USER=macxxn
IMAGE_NAME=lepv
IMAGE_TAG=flask

CONTAINER_NAME=lepv
CONTAINER_PORT=5000
HOST_BIND_PORT=9955
######################################

echo "running containers:"
docker ps
echo ""

echo "stop and remove existing container below:"
docker rm -f ${CONTAINER_NAME}

echo ""
echo "port mapping:"
echo "host:container = "${HOST_BIND_PORT}":"${CONTAINER_PORT}
echo ""

docker run -p ${HOST_BIND_PORT}:${CONTAINER_PORT} --name ${CONTAINER_NAME} -t ${DOCKER_USER}/${IMAGE_NAME}':'${IMAGE_TAG}
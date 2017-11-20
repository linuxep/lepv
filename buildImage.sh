#!/bin/bash

which docker-compose > /dev/null 2>&1
if [ $? == 0 ]; then
    echo "docker-compose exist"
else
    curl -L https://get.daocloud.io/docker/compose/releases/download/1.17.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
	chmod +x /usr/local/bin/docker-compose
fi
docker-compose build

# echo "Generated docker image = ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
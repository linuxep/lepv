#! /bin/bash
echo "add Mainland Registry Mirror"
#echo "DOCKER_OPTS=\" --registry-mirror=http://3d9b08b6.m.daocloud.io\"" | sudo tee -a /etc/default/docker 
curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://3d9b08b6.m.daocloud.io
sudo service docker restart

echo "Building docker image"
docker build -f docker/Dockerfile -t linuxep/lepv0.1 .

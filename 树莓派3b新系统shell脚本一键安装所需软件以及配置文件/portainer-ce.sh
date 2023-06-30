#!/bin/bash

docker pull portainer/portainer-ce

#创建 portainer 容器
sudo docker volume create portainer_data
#运行 portainer
sudo docker run -d -p 10000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
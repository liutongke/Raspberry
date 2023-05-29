#!/bin/bash

# 构建 Docker 镜像
docker build -t monitor_nvr:v1 .

# 运行 Docker 容器
docker run --name monitor_nvr-v1 -itd  -p 9090:9090/udp monitor_nvr:v1

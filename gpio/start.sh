#!/bin/bash

# 构建 Docker 镜像
docker build -t go-ffmpeg:v1 .

# 运行 Docker 容器
docker run --name go-ffmpeg-v1 -itd -p 9090:9090/udp go-ffmpeg:v1

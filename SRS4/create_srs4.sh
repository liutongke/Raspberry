#!/bin/bash

docker run -itd --name srs4-cow registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4

docker cp srs4-cow:/usr/local/srs/conf ./

docker build -t srs4:v1 .

VIDEO_DIR="video"
if [ ! -d "$VIDEO_DIR" ]; then
    mkdir "$VIDEO_DIR"
fi

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run --name srs4-v1 -itd -p 1935:1935 -p 1985:1985 -p 8080:8080 --restart always -v "$SCRIPT_PATH/conf":/usr/local/srs/conf -v "$SCRIPT_PATH/video":/usr/local/srs/video srs4:v1 ./objs/srs -c conf/docker.conf

docker stop srs4-cow

docker rm srs4-cow

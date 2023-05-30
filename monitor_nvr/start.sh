#!/bin/bash

current_dir=$(pwd)
data_dir="$current_dir/data"

# 检查目录是否存在
if [ -d "$data_dir" ]; then
  echo "目录已存在: $data_dir"
else
  # 创建目录
  mkdir "$data_dir"
  echo "创建目录: $data_dir"
fi

# 构建 Docker 镜像
docker build -t monitor_nvr:v1 .

# 运行 Docker 容器
docker run --name monitor_nvr-v1 -itd -p 9090:9090/udp -v $data_dir:/var/www/html/data monitor_nvr:v1

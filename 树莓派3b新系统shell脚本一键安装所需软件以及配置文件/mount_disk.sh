#!/bin/bash

# 检查目标挂载点是否存在，如果不存在则创建
if [ ! -d "/media/keke" ]; then
  sudo mkdir /media/keke
fi

# 挂载硬盘
sudo mount /dev/sda1 /media/keke/

# 检查挂载是否成功
if [ $? -eq 0 ]; then
  echo "硬盘挂载成功"
else
  echo "硬盘挂载失败"
fi

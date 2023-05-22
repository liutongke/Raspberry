#!/bin/bash

# 删除源
rm "/etc/apt/sources.list"
rm "/etc/apt/sources.list.d/raspi.list"

# 替换新源
cp "./sources.list" "/etc/apt/sources.list"
cp "./raspi.list" "/etc/apt/sources.list"

# 执行更新命令
sudo apt-get update

# 执行升级命令
sudo apt-get upgrade -y

# 下载 get-docker.sh 脚本
sudo curl -fsSL https://get.docker.com -o get-docker.sh

# 执行 get-docker.sh 脚本
sudo sh get-docker.sh

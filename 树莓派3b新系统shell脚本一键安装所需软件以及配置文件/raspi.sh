#!/bin/bash
#自动化更新国内源、安装docker、安装syncthing、安装supervisord并设置开机启动

#lite无桌面版本，要在更换国内源之前执行
sudo apt install python3-pip -y

# 修改 sources.list 文件
sudo tee /etc/apt/sources.list >/dev/null <<EOL
deb https://mirrors.tuna.tsinghua.edu.cn/debian buster main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security/ buster/updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian buster-updates main contrib non-free
EOL

#sudo tee /etc/apt/sources.list >/dev/null <<EOL
#deb https://mirrors.tuna.tsinghua.edu.cn/debian buster main contrib non-free
#deb https://mirrors.tuna.tsinghua.edu.cn/debian-security/ buster/updates main contrib non-free
#deb https://mirrors.tuna.tsinghua.edu.cn/debian buster-updates main contrib non-free
#EOL

# 修改 raspi.list 文件
sudo sed -i 's|^deb .*|deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui|' /etc/apt/sources.list.d/raspi.list
sudo sed -i 's|^deb-src .*|deb-src http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui|' /etc/apt/sources.list.d/raspi.list

#sudo sed -i 's|^deb .*|deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui|' /etc/apt/sources.list.d/raspi.list
#sudo sed -i 's|^deb-src .*|deb-src http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui|' /etc/apt/sources.list.d/raspi.list

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install unzip lrzsz -y

if sudo docker version &>/dev/null; then
  echo "Docker已成功安装"
else
  #树莓派安装docker
  sudo curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
fi

#设置 Docker 开机启动
sudo systemctl enable docker
#开启 Docker 服务
sudo systemctl start docker

#sudo docker run hello-world

#下载 Docker 图形化界面 portainer
#sudo docker pull portainer/portainer
#创建 portainer 容器
#sudo docker volume create portainer_data
#运行 portainer
#sudo docker run -d -p 10000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer

mkdir -p /var/www/html
mkdir -p /var/www/nginx

if [ -d "/var/www/html/pi-dashboard-master" ]; then
  echo "文件夹存在"
else
  echo "文件夹不存在"

  if [ -f "master.zip" ]; then
    echo "文件存在"
  else
    echo "master.zip文件不存在"
    wget https://github.com/nxez/pi-dashboard/archive/refs/heads/master.zip
  fi
  sudo unzip master.zip
  mv $(pwd)/pi-dashboard-master /var/www/html/
  cp $(pwd)/pi-dashboard.conf /var/www/nginx
fi

#创建bridge网络
#sudo docker network create pi-dashboard-net
#创建nginx
#sudo docker run --name nginx1 --network pi-dashboard-net --network-alias pi-dashboard-nginx --restart always -p 80:80 -v /var/www/html:/usr/share/nginx/html -v /var/www/nginx:/etc/nginx/conf.d -d nginx
#创建php
#sudo docker run --name php1 --network pi-dashboard-net --network-alias pi-dashboard-php --restart always -p 9000:9000 -v /var/www/html:/var/www/html -d php:8.1.18-fpm

if [ -f "/home/keke/.config/syncthing/config.xml" ]; then
  echo "syncthing已经安装"
else
  file="syncthing-linux-arm64-v1.23.4.tar.gz"

  if ! [ -f "$file" ]; then
    echo "文件 $file 不存在"
    wget https://github.com/syncthing/syncthing/releases/download/v1.23.4/syncthing-linux-arm64-v1.23.4.tar.gz
  fi

  tar -zxvf syncthing-linux-arm64-v1.23.4.tar.gz

  #syncthing-linux-arm64-v1.23.4
  mv syncthing-linux-arm64-v1.23.4 $(pwd)/syncthing

  # 指定用户和程序
  username=keke
  program=$(pwd)/syncthing/syncthing

  # 切换到指定用户，并后台运行程序
  sudo -u "$username" nohup "$program" >/dev/null 2>&1 &
fi

echo "暂停5秒"
# 暂停5秒
sleep 5
echo "暂停结束，继续执行脚本"

#启动成功以后杀掉
# 查找syncthing进程的PID
pid=$(pgrep syncthing)

if [ -n "$pid" ]; then
  # 发送终止信号给syncthing进程
  kill "$pid"
  echo "Syncthing进程已成功终止"
else
  echo "Syncthing进程未运行"
fi

file=$(pwd)"/.config/syncthing/config.xml"
search="<address>127.0.0.1:8384</address>"
replace="<address>0.0.0.0:8384</address>"

sed -i "s|$search|$replace|g" "$file"
echo "$file 配置已成功配置"

#pip配置国内源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
sudo pip install supervisor

sudo mkdir -p /etc/supervisor
sudo mkdir -p /etc/supervisor/conf.d
sudo mkdir -p /var/log/supervisor/
sudo mkdir -p $(pwd)/log

sudo cp $(pwd)/supervisord.conf /etc/supervisor
sudo cp $(pwd)/syncthing.conf /etc/supervisor/conf.d
echo "启动supervisord"
#设置开启启动
#sudo supervisord -c /etc/supervisor/supervisord.conf
# 将命令添加到rc.local文件中
sudo sed -i '/exit 0/d' /etc/rc.local
sudo sed -i '/^fi$/a sudo supervisord -c /etc/supervisor/supervisord.conf' /etc/rc.local
sudo echo 'exit 0' | sudo tee -a /etc/rc.local

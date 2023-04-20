# 树莓派（Raspberry Pi）学习资料总结
>前言：写这份总结目的是树莓派吃灰几年一直运行docker在家当作开发测试的数据库使用，导致之前买的硬件都没有得到充分的利用，再加上以前零零碎碎写的资料不完整、包括开发的Python脚本丢失，比如小车的L298N电机驱动板之前踩过不少坑当时也没能留下资料，包括接线图也没保存。所以决定对这些资料进行重新总结汇总，以便以后查看，以下内容均基于树莓派3b（Raspberry Pi 3b）。

**系统版本：Raspberry Pi OS 64 位（Raspbian）**

# Go编译树莓派运行程序

```sh
SET CGO_ENABLED=0
SET GOOS=linux
SET GOARCH=arm64
SET GOARM=7
go build -o tinypng main.go Tinypng.go
```

# windwos11系统使用PyCharm开发GPIO

为了提高代码提示的效率，在本地开发环境中使用[RPi.GPIO-def](https://pypi.org/project/RPi.GPIO-def/0.1.1-alpha/)包可以是一个好的替代方案，该包包含了RPi.GPIO库的函数定义，可以让代码编辑器正确地识别函数和参数，提供更好的代码提示。

然而，需要注意的是，[RPi.GPIO-def](https://pypi.org/project/RPi.GPIO-def/0.1.1-alpha/)包只是一个函数定义的包，它并不包含实际的GPIO硬件控制功能。因此，如果需要在实际的硬件上运行代码，还需要使用RPi.GPIO库，并在树莓派上安装该库。

另外，如果需要在本地开发环境中模拟GPIO硬件功能，可以考虑使用第三方模拟器，例如GPIO Zero。这样可以在本地开发环境中测试代码，而无需连接实际的硬件设备。

[RPi.GPIO-def](https://pypi.org/project/RPi.GPIO-def/0.1.1-alpha/)安装

```cmd
pip install RPi.GPIO-def==0.1.1-alpha
```


![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/202304151139306.png)

PyCharm演示：
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/202304151140877.png)

# 新装系统初始化开启ssh和连接WiFi设置
raspbian系统默认ssh为关闭状态，最简单的开启方法是在内存卡根目录下建个名为ssh的文件，放入树莓派重启就会自启ssh服务了。

即在boot目录中创建名为ssh的txt文档 ssh.txt 然后将后缀名.txt删除



新建文件，文件名为wpa_supplicant.conf
```sh
country=CN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
 
network={
 ssid=""
 psk=""
key_mgmt=WPA-PSK
priority=1
}
```
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/202304151630549.png)


根据 Raspberry Pi OS Bullseye 的4月更新说明，经典的 pi 用户名和 raspberry 已经被取消，用户想要使用树莓派通过HDMI连接显示器设置初始化。

# 树莓派更换国内清华源

树莓派的所有软件源地址：https://www.raspbian.org/RaspbianMirrors

64位Pi OS

修改 sources.list 文件，用以下内容替换：
```sh
sudo vi /etc/apt/sources.list
deb https://mirrors.tuna.tsinghua.edu.cn/debian buster main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security/ buster/updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian buster-updates main contrib non-free
```


修改 raspi.list 文件，用以下内容替换：

```sh
sudo vi /etc/apt/sources.list.d/raspi.list
deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui
```


3. 同步更新源、软件包
执行以下命令：
```sh
sudo apt-get update
sudo apt-get upgrade
```

# 树莓派安装docker

```sh
sudo curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

安装成功界面
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/202304151717893.png)


测试 Docker
运行 hello-world 镜像来做一个测试。

```sh
sudo docker run hello-world
```

如果 Docker 安装成功，你会看到一条消息：“Hello from Docker!”。

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/202304151719804.png)

常用配置和工具命令
```sh

#查看 Docker 版本
docker -v
sudo docker pull 仓库/镜像:版本（留空的话默认为 latest）
sudo docker run 加参数，用来创建容器
#查看运行容器
sudo docker ps
#查看所有下载的镜像
sudo docker images
#进入容器终端
sudo docker exec -i -t ha /bin/bash
#实时查看10行的 ha 日志
sudo docker logs -f -t --tail 10 ha
#重启 systemctl 守护进程
sudo systemctl daemon-reload
#设置 Docker 开机启动
sudo systemctl enable docker
#开启 Docker 服务
sudo systemctl start docker
 
#下载 Docker 图形化界面 portainer
sudo docker pull portainer/portainer
#创建 portainer 容器
sudo docker volume create portainer_data


```

# 安装php、nginx、MySQL、Redis
```
docker run --name mysql-v1 -p 3306:3306 --restart always -v /var/www/MySQL/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=xCl5QUb9ES2YfkvX -d mysql:8.0
docker run --name nginx1 --restart always -p 80:80 -v /var/www/html:/usr/share/nginx/html -v /var/www/nginx:/etc/nginx/conf.d -d nginx
docker run --name php1 --restart always -p 9000:9000 -v /var/www/html:/var/www/html -d php:8.1.18-fpm
docker run -d --name redis-1 --restart always -p 6379:6379 redis

#运行 portainer
sudo docker run -d -p 10000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
```

# 树莓派root登陆：

```sh
sudo passwd root            #设置root用户密码
sudo passwd --unlock root   #开启root账户
su root                     #测试是否生效
```
重新锁定root账户可执行命令：sudo passwd --lock root

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/202304151759701.png)

# 树莓派开机发送邮件

```
sudo vi /etc/rc.local
```
在`exit0`前添加python开机需要执行的脚本`SendToEmailLocalIp.py`

```sh
sudo python /var/www/SendToEmailLocalIp.py
```

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/202304161546925.png)

# 通过docker搭建PHP8.1+nginx搭建环境

```
docker run --name nginx1 -p 8080:80 -v /var/www/html:/usr/share/nginx/html -v /var/www/nginx:/etc/nginx/conf.d -d nginx #安装nginx

docker run --name php1 -p 9000:9000 -v /var/www/html:/var/www/html -d php:8.1.18-fpm    #安装PHP
```

nginx中配置文件目录

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230416211427.png)

nginx.conf配置
```
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    location ~ \.php$ {
        root /var/www/html/;#增加PHP服务器的目录
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass 192.168.1.107:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}

```

# syncthing

[syncthing下载地址](https://syncthing.net/downloads/)

配置文件目录
/home/keke/.config/syncthing/config.xml

修改访问权限
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230417125121.png)

启动软件
/home/keke/syncthing/syncthing

```
#! /bin/bash
/home/keke/syncthing/syncthing
```


# PLC编程上升沿与下降沿
上升沿就是从0变成1中间的过程。

下降沿就是从1变成0中间的过程。
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230420180040.png)


结论：上升沿：常开到闭合触发的瞬间执行！

下降沿：常闭到断开的瞬间执行。上升沿就像点动启动按钮，下降沿就像点动停止按钮!
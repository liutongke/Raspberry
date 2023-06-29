# 树莓派（Raspberry Pi）学习资料总结
>前言：写这份总结目的是树莓派吃灰几年一直运行docker在家当作开发测试的数据库使用，导致之前买的硬件都没有得到充分的利用，再加上以前零零碎碎写的资料不完整、包括开发的Python脚本丢失，比如小车的L298N电机驱动板之前踩过不少坑当时也没能留下资料，包括接线图也没保存。所以决定对这些资料进行重新整理总结汇总，以便以后查看。

**开发板：树莓派3b（Raspberry Pi 3b）**
**系统版本：Raspberry Pi OS 64 位（Raspbian）**

# 查看摄像头

<span style="color: red;"><span style="font-size: 24px;">树莓派3b刷完新系统不需要任何设置，默认打开`libcamera`，不需要`sudo raspi-config
`中打开摄像头，调用摄像头指示灯，都属于正常现象。也不要使用国内源设置，否则安装blinker后会导致`libcamera`失效报错</span></span>

```sh
ls /dev/video*
```

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230427151415.png)

## Streaming Video 直播视频
树莓派输入：
```sh
libcamera-vid -t 0 --inline --listen -o tcp://0.0.0.0:8888
```
播放器输入
```sh
tcp/h264://树莓派地址:8888
```

```sh
vcgencmd get_camera
```
**supported = 1 detected = 0
supported = 0未开启摄像头
detected = 0 表明没有接入摄像头设备**
设置新版摄像头的话detected就为0无法使用ffmpeg推流

# 查看摄像头返回数据格式
树莓派摄像头 `/dev/video0` 返回的是视频流数据，通常是以图像帧的形式传输。每一帧可以使用不同的图像格式进行编码，例如常见的 JPEG、YUV、RGB 等。

要确定 `/dev/video0` 返回的确切格式，你可以使用一些图像处理库或工具来读取并解码视频帧。在 Linux 上，你可以使用 `v4l-utils` 包中的工具来获取有关视频流的详细信息。以下是一个使用 `v4l2-ctl` 命令查看 `/dev/video0` 格式的示例：

```
sudo apt install v4l-utils -y

v4l2-ctl --list-formats-ext -d /dev/video0
```

该命令将显示有关 `/dev/video0` 支持的不同格式、分辨率和帧率的信息。

请注意，具体的视频格式可能会根据你的系统配置、摄像头型号以及所使用的驱动程序而有所不同。因此，确切的格式可能会因情况而异。

# 新版报错系统设置摄像头

调用`libcamera`命令拍照出现<span style="color: red;">**`ERROR: the system appears to be configured for the legacy camera stack
`**</span>报错，这是由于在最新的树莓派系统中已经从基于专有 Broadcom GPU 代码的传统相机软件堆栈过渡到基于libcamera的开源堆栈，也就说未来会使用libcamera来替代。libcamera是一个旨在直接从Linux操作系统支持复杂的相机系统的软件库。对于Raspberry Pi，它使我们能够直接从在ARM处理器上运行的开源代码驱动相机系统。

### 解决方法

在`/boot/config.txt`文件中添加`dtoverlay`字段
```
sudo sed -i '/^display_auto_detect=1$/a dtoverlay=ov5647' /boot/config.txt
```

![根据摄像头配置](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230427121348.png)

#### [dtoverlay字段与摄像头对照表](https://www.raspberrypi.com/documentation/computers/camera_software.html)：如下

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230427121445.png)
查看PCF8591器件的地址(硬件地址 由器件决定) 


保存视频十秒钟的视频
```sh
libcamera-vid -t 10000 -o test.h264
```

拍摄照片
```sh
libcamera-jpeg -o test.jpg
```

# 使用Picamera2拍照
[Picamera2 手册中](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
[Python 绑定libcamera](https://www.raspberrypi.com/documentation/computers/camera_software.html#python-bindings-for-libcamera)
## 快速拍照并保存，不需要预览
```python
from picamera2 import Picamera2, Preview
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()
picam2.capture_file("test.jpg")
```

## 快速录制视频并保存，不需要预览
```python
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.start_and_record_video("test.mp4", duration=5) #视频格式mp4,长度5秒
```

## OSError: libmmal.so: cannot open shared object file: No such file or directory
https://segmentfault.com/a/1190000040009665

# Windwos使用工具

https://learn.microsoft.com/zh-cn/sysinternals/downloads/tcpview

# Linux命令
在 `free -h` 命令输出中，以下是每个字段的含义：

- `total`：物理内存的总量，包括系统保留的和已分配的内存。
- `used`：已使用的物理内存量，包括被应用程序和系统进程占用的内存。
- `free`：空闲的物理内存量，可立即用于分配给新进程。
- `shared`：被共享的内存量，多个进程共享的内存。
- `buff/cache`：用于磁盘缓存和缓冲区的内存量。它包括内核使用的缓存和文件系统缓存。
- `available`：当前可用的内存量，表示系统可以立即分配给新进程或已存在进程使用的内存。它包括未被系统保留的空闲内存和被操作系统缓存和缓冲区占用的内存。


在 Debian 系统中，`top` 命令输出中的进程号 USER PR NI VIRT RES SHR %CPU %MEM TIME+ COMMAND 字段的含义如下：

- `PID`：进程的标识符。
- `USER`：启动进程的用户名。
- `PR`：进程的优先级。
- `NI`：进程的优先级别值。
- `VIRT`：进程使用的虚拟内存大小（单位：KB）。
- `RES`：进程使用的物理内存大小（单位：KB）。
- `SHR`：进程使用的共享内存大小（单位：KB）。
- `%CPU`：进程使用的 CPU 百分比。
- `%MEM`：进程使用的内存百分比。
- `TIME+`：进程累计的 CPU 使用时间。
- `COMMAND`：启动进程的命令行。


# 安装Go
```
wget https://go.dev/dl/go1.20.5.linux-arm64.tar.gz

sudo tar -C /usr/local/ -zxvf go1.20.5.linux-arm64.tar.gz

#在`~/.bashrc`文件的末尾添加以下内容：
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
echo 'export GOPATH=$HOME/go' >> ~/.bashrc

然后，您需要更新当前终端的环境变量，使新添加的内容生效。可以运行以下命令来实现：
source ~/.bashrc

验证
echo $GOPATH
```
重启系统后`go versioin`验证。

## Go更换源

```sh
#配置 GOPROXY 环境变量：
go env -w GOPROXY=https://goproxy.cn,direct

#验证：
go env | grep GOPROXY

#测试：
time go get golang.org/x/tour
```


本地如果有模块缓存，可以使用命令清空`go clean --modcache`

# Go编译树莓派运行程序：

```sh
SET CGO_ENABLED=0
SET GOOS=linux
SET GOARCH=arm64
SET GOARM=7
go build -o tinypng main.go Tinypng.go
```

# Python更换软连接 {#apt-get-pip}
```sh
cd /usr/bin

ls -al *python*

sudo rm python

ln -s python3.9
```

[参考连接](https://blog.csdn.net/qq_42887760/article/details/100997264)

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230624220831.png)

# Python更换国内源

```sh
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```
/home/keke/.config/pip/pip.conf
# lite版本系统python3安装pip

要在更换国内源之前执行
```sh
sudo apt install python3-pip
```


# Windows11系统使用PyCharm开发GPIO

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

## 使用官方系统工具刷系统，初始化系统
使用官方提供的系统安装工具（Raspberry Pi Imager）在刷系统的时候可以通过「设置」来指定用户名和密码。[Raspberry Pi Imager下载地址](https://www.raspberrypi.com/software/)

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230623055329.png)


# 树莓派更换国内源

<span style="font-size: 24px;"><span style="color: rgb(255, 41, 65); font-size: 24px;">**如果想同时安装blinker-py和使用libcamera摄像头则不能更换国内源**</span></span>

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

```sh
# 修改 sources.list 文件
sudo tee /etc/apt/sources.list >/dev/null <<EOL
deb https://mirrors.tuna.tsinghua.edu.cn/debian buster main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security/ buster/updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian buster-updates main contrib non-free
EOL

# 修改 raspi.list 文件
sudo sed -i 's|^deb .*|deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui|' /etc/apt/sources.list.d/raspi.list
sudo sed -i 's|^deb-src .*|deb-src http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui|' /etc/apt/sources.list.d/raspi.list
```


# 树莓派安装Docker

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

# Docker更换国内源,新建或者修改`/etc/docker/daemon.json`
```
{
    "registry-mirrors": [
        "https://dockerproxy.com",
        "https://docker.nju.edu.cn",
        "https://docker.mirrors.sjtug.sjtu.edu.cn"
    ]
}
```

# 安装php、nginx、MySQL、Redis
```sh
sudo docker run --name mysql-v1 -p 3306:3306 --restart always -v /var/www/MySQL/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=xCl5QUb9ES2YfkvX -d mysql:8.0
sudo docker run --name nginx1 --restart always -p 80:80 -v /var/www/html:/usr/share/nginx/html -v /var/www/nginx:/etc/nginx/conf.d -d nginx
sudo docker run --name php1 --restart always -p 9000:9000 -v /var/www/html:/var/www/html -d php:8.1.18-fpm
sudo docker run -d --name redis-1 --restart always -p 6379:6379 redis

#运行 portainer
sudo docker run -d -p 10000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
```

# 安装pi-dashboard

[pi-dashboard下载地址：](https://github.com/nxez/pi-dashboard)

旧版本`portainer`，官方已停止维护。
```sh
#创建bridge网络
docker network create pi-dashboard-net 

#创建nginx
sudo docker run --name nginx1 --network pi-dashboard-net --network-alias pi-dashboard-nginx --restart always -p 80:80 -v /var/www/html:/usr/share/nginx/html -v /var/www/nginx:/etc/nginx/conf.d -d nginx
#创建php（绑定宿主机名称让容器内可或者正确hostname）
sudo docker run --name php2 --network pi-dashboard-net --network-alias pi-dashboard-php --restart always -p 9000:9000 -v /var/www/html:/var/www/html -v /etc/hostname:/etc/hostname -d php:8.1.18-fpm

#将nginx移除mynet局域网络
docker network disconnect 创建的bridge 对应的network-alias

```

使用新版本`portainer-ce`一键安装sh脚本：
```sh
#!/bin/bash

docker pull portainer/portainer-ce

#创建 portainer 容器
sudo docker volume create portainer_data
#运行 portainer
sudo docker run -d -p 10000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
```
## 一键安装PHP+nginx脚本：
```sh
#!/bin/bash

#创建bridge网络
docker network create pi-dashboard-net

#创建nginx
sudo docker run --name nginx1 --network pi-dashboard-net --network-alias pi-dashboard-nginx --restart always -p 80:80 -v /var/www/html:/usr/share/nginx/html -v /var/www/nginx:/etc/nginx/conf.d -d nginx

hostip=$(hostname -I | awk '{print $1}')
echo $hostip
#创建php（绑定宿主机名称让容器内可或者正确hostname）-e MY_IP绑定宿主机ip
sudo docker run --name php1 -e MY_IP="$hostip" --network pi-dashboard-net --network-alias pi-dashboard-php --restart always -p 9000:9000 -v /var/www/html:/var/www/html -v /etc/hostname:/etc/hostname -d php:8.1.18-fpm

```

## pi-dashboard.conf配置文件：

```nginx
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    location ~ \.php$ {
        root /var/www/html/;#增加PHP服务器的目录
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass pi-dashboard-php:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}


```
# 通过Docker搭建PHP8.1+nginx搭建环境

```
docker run --name nginx1 -p 8080:80 -v /var/www/html:/usr/share/nginx/html -v /var/www/nginx:/etc/nginx/conf.d -d nginx #安装nginx

docker run --name php1 -p 9000:9000 -v /var/www/html:/var/www/html -d php:8.1.18-fpm    #安装PHP
```

nginx中配置文件目录

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230416211427.png)

nginx.conf配置
```nginx
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



# syncthing

[syncthing下载地址](https://syncthing.net/downloads/)

第一步：切入到syncthing项目，执行命令启动下软件
第二步：配置文件目录修改访问权限，可以非本机用户访问
/home/keke/.config/syncthing/config.xml

修改访问权限
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230417125121.png)

第三步：启动软件
/home/keke/syncthing/syncthing

```
#! /bin/bash
/home/keke/syncthing/syncthing
```

访问地址：
`http://user ip:8384/`

# 安装Supervisord并且开机启动syncthing

## 安装Supervisord
- [x] **apt-get安装方式：** Raspberry Pi OS 64 位系统下：`sudo apt-get install supervisor`，通过这种方式安装后，系统自动设置为开机启动。**此种安装方法会变更系统的python3绑定软连接**
- [x] **pip安装方式（推荐）：** Raspberry Pi OS 64 位系统下，[桌面版有pip，lite版本没有pip需要自己安装](#apt-get-pip)

1. pip安装supervisor
```sh
sudo pip install  supervisor
```
2. 创建文件夹并上传配置文件到对应的文件夹，配置文件也可以通过命令行生成
```

sudo mkdir -p /etc/supervisor/conf.d
sudo mkdir -p /home/keke/supervisor_log
sudo mkdir -p /var/log/supervisor

```


![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230421173449.png)


3. 启动supervisord
```sh
sudo supervisord -c /etc/supervisor/supervisord.conf
```
4. 设置开机自启动supervisord
```sh
# 将命令添加到rc.local文件中
sudo sed -i '/exit 0/d' /etc/rc.local
sudo sed -i '/^fi$/a sudo supervisord -c /etc/supervisor/supervisord.conf' /etc/rc.local
sudo echo 'exit 0' | sudo tee -a /etc/rc.local
```

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230421173241.png)


## Supervisord配置Syncthing

Syncthing文档[Using Supervisord](https://docs.syncthing.net/users/autostart.html?highlight=home#using-supervisord) 地址

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230421131519.png)

`/etc/supervisor/conf.d`目录中创建`syncthing.conf`配置文件，配置参考如下：

```supervisor
[program:syncthing] ; 程序名称，在 supervisorctl 中通过这个值来对程序进行一系列的操作
autorestart=True      ; 程序异常退出后自动重启
autostart=True        ; 在 supervisord 启动的时候也自动启动
redirect_stderr=True  ; 把 stderr 重定向到 stdout，默认 false
environment=STNORESTART="1", HOME="/home/keke"  ; 可以通过 environment 来添加需要的环境变量，一种常见的用法是使用指定的 virtualenv 环境
command=/home/keke/syncthing/syncthing --no-browser --home="/home/keke/.config/syncthing" ; 启动命令，与手动在命令行启动的命令是一样的
user=keke           ; 用哪个用户启动
directory=/home/keke/syncthing/  ; 程序的启动目录
stdout_logfile_maxbytes = 20MB  ; stdout 日志文件大小，默认 50MB
stdout_logfile_backups = 20     ; stdout 日志文件备份数
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile = /home/keke/log/usercenter_stdout.log
```

点灯配置文件`blinker`:
```supervisor
[program:blinker] ; 程序名称，在 supervisorctl 中通过这个值来对程序进行一系列的操作
autorestart=True      ; 程序异常退出后自动重启
autostart=True        ; 在 supervisord 启动的时候也自动启动
redirect_stderr=True  ; 把 stderr 重定向到 stdout，默认 false
environment=STNORESTART="1", HOME="/home/keke"  ; 可以通过 environment 来添加需要的环境变量，一种常见的用法是使用指定的 virtualenv 环境
command=python3 /var/www/blinker/main.py ; 启动命令，与手动在命令行启动的命令是一样的
user=root           ; 用哪个用户启动
directory=/var/www/blinker/  ; 程序的启动目录
stdout_logfile_maxbytes = 20MB  ; stdout 日志文件大小，默认 50MB
stdout_logfile_backups = 20     ; stdout 日志文件备份数
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile = /home/keke/log/blinker.log
```

位于`/etc/supervisor`路径中的`supervisord.conf`配置：

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230624142237.png)

```supervisor
; supervisor config file

[unix_http_server]
file=/var/run/supervisor.sock   ; (the path to the socket file)
chmod=0700                       ; sockef file mode (default 0700)

[supervisord]
logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
childlogdir=/var/log/supervisor            ; ('AUTO' child log dir, default $TEMP)

; the below section must remain in the config file for RPC
; (supervisorctl/web interface) to work, additional interfaces may be
; added by defining them in separate rpcinterface: sections
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///var/run/supervisor.sock ; use a unix:// URL  for a unix socket

; The [include] section can just contain the "files" setting.  This
; setting can list multiple files (separated by whitespace or
; newlines).  It can also contain wildcards.  The filenames are
; interpreted as relative to this file.  Included files *cannot*
; include files themselves.

[include]
files = /etc/supervisor/conf.d/*.conf

```


## supervisorctl常用操作命令

```sh
sudo supervisorctl reload            #重启Supervisord
sudo supervisorctl start syncthing   #启动Supervisord
sudo supervisorctl status syncthing  #检查Supervisord状态
sudo supervisorctl tail syncthing    #检查Supervisord日志
```


# PLC编程上升沿与下降沿
上升沿就是从0变成1中间的过程。

下降沿就是从1变成0中间的过程。
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230420180040.png)


结论：上升沿：常开到闭合触发的瞬间执行！

下降沿：常闭到断开的瞬间执行。上升沿就像点动启动按钮，下降沿就像点动停止按钮!

# 挂载NTFS磁盘
![磁盘被程序占用](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230421200255.png)

```
sudo apt-get install ntfs-3g            #下载支持的依赖
sudo fdisk -l                           #查看磁盘信息
sudo fuser -m /dev/sda1                 #查看占用的进程（磁盘被程序占用）
sudo mount /dev/sda1 /home/keke/disk1/  #挂载磁盘
```

# [调整swap分区大小](https://www.cnblogs.com/varden/p/15409542.html)



# [SSD1306.py 函数](https://pypi.org/project/micropython-ssd1306py/)

1. text(string, x, y)，在(x, y)处显示字符串，注意text()函数内置的字体是8x8的，暂时不能替换
1. poweroff()，关闭OLED显示
1. poweron()，空函数，无任何效果。可以用 write_cmd(0xAF) 代替
1. fill(n)，n=0，清空屏幕，n大于0，填充屏幕
1. contrast()，调整亮度。0最暗，255最亮
1. invert()，奇数时反相显示，偶数时正常显示
1. pixel(x, y, c)，在(x, y)处画点
1. show()，更新显示内容。前面大部分函数只是写入数据到缓冲区，并不会直接显示到屏幕，需要调用show()后才能显示出来。
1. framebuf.line(x1,y1,x2,y2,c)，画直线
1. framebuf.hline(x,y,w,c)，画水平直线
1. framebuf.vline(x,y,w,c)，画垂直直线
1. framebuf.fill_rect(x,y,w,h,c)，画填充矩形
1. framebuf.rect(x,y,w,h,c)，画空心矩形


# i2c是共享总线，只要没有两个设备共享dame i2c地址，就允许多个设备并联
Re: Both devices need to use SDA and SCL
Fri Dec 20, 2019 5:10 pm

I2C is a bus. Multiple devices may be connected in parallel.


GY30模块（BH1750FVI光线传感器）

sudo i2cdetect -y 1

# adafruit_pcf8591

[Installing Blinka on Raspberry Pi](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)

`NameError: name 'PCF8591' is not defined`报错，将
`/usr/local/lib/python3.9/dist-packages/adafruit_pcf8591`位置中的`analog_in.py、analog_out.py`文件修改如下图：
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230502190628.png)
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230502190642.png)


# ThinkAPI统一API接口服务
https://www.kancloud.cn/topthink-doc/think-api/1861639


# 获取本机公网ip地址


```sh
http://ip.42.pl/raw
https://api.ip.sb/ip
http://ip.3322.net
http://ip.qaros.com
http://ip.cip.cc
http://ident.me
http://icanhazip.com
https://api.ipify.org
https://api64.ipify.org?format=json
```


# 安装使用samba
```sh
sudo apt-get install samba
# 如果安装失败卸载冲突依赖
sudo apt-get install autoremove 对应的依赖包名称

# 重启服务
sudo /etc/init.d/smbd restart
​
# 查看服务状态
sudo /etc/init.d/smbd status

# 开机自启动
sudo systemctl enable smbd

# 修改用户密码
sudo smbpasswd -a 用户名
```

`autoremove`命令不存在情况下可以改用`sudo apt remove 对应的包名称`
配置目录位置：
```sh
/etc/samba
```

```sh
各参数意思
[kingston]：分享名称
comment：备注描述
path：共享文件夹目录
writable：是否可写入，不能写入就不能创建文件夹
browseable：是否可以访问浏览
valid user：允许哪个用户访问，这里需要按照指定的账户访问samba服务
```



![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230621123727.png)


`/etc/samba/smb.conf`末尾添加
```sh
[keke]
path = /var/www/
valid users = keke
browseable = Yes
writeable = Yes
writelist = keke
create mask = 0777
directory mask = 0777
```


- [keke]：定义了一个共享名称为 "keke" 的共享文件夹。
- path = /var/www/：指定了共享文件夹的路径为 /var/www/，即根据该配置，共享的内容位于 /var/www/ 目录下。
- valid users = keke：指定了允许访问该共享文件夹的有效用户为 "keke"，只有该用户可以访问共享。
- browseable = Yes：设置共享文件夹可浏览，其他用户可以看到该共享。
- writeable = Yes：设置共享文件夹可写入，允许用户对共享进行写操作。
- writelist = keke：指定了允许写入共享文件夹的用户为 "keke"，只有该用户可以写入文件。
- create mask = 0777：设置新创建的文件的权限掩码为 0777，即所有用户对新创建的文件具有读、写和执行的权限。
- directory mask = 0777：设置新创建的目录的权限掩码为 0777，即所有用户对新创建的目录具有读、写和执行的权限。

这段配置文件的作用是创建一个名为 "keke" 的共享文件夹，允许用户 "keke" 访问，并且只有该用户可以写入文件夹。其他用户可以浏览文件夹内容，但没有写入权限。创建的文件和目录都具有广泛的权限，所有用户都可以读取、写入和执行。

配置完修改密码：
```
sudo smbpasswd -a keke
```

windows **网络->映射磁盘驱动器**，输入以下内容，然后输入账号密码登录：
```
\\192.168.1.107\keke
```


sudo mount /dev/sda1 /media/keke/


# 用UDP协议发送时，用sendto函数最大能发送数据的长度为：65535- IP头(20) - UDP头(8)＝65507字节


# 两个TS视频文件能够连续播放的条件

在 HLS（HTTP Live Streaming）协议中，要实现两个 TS（Transport Stream）文件之间的平滑衔接，需要满足以下要求：

1. 相邻两个 TS 文件的时间戳连续：每个 TS 文件中的视频和音频帧都包含时间戳信息。确保相邻的 TS 文件中的时间戳是连续的，即当前 TS 文件的最后一个帧的时间戳和下一个 TS 文件的第一个帧的时间戳是连贯的。

2. PTS（Presentation Time Stamp）和 DTS（Decoding Time Stamp）的一致性：在 TS 文件中，视频帧和音频帧分别具有 PTS 和 DTS。确保相邻 TS 文件中的视频和音频帧的 PTS 和 DTS 是一致的，以保证平滑的切换和连续的播放。

3. I帧（关键帧）的位置：在衔接两个 TS 文件时，最好在衔接点附近使用 I 帧（关键帧）。这样可以确保衔接处的画面质量较高，减少画面的失真或断裂。

4. 播放器缓冲控制：播放器在播放 TS 文件时通常会使用缓冲机制，以提供流畅的播放体验。确保播放器的缓冲设置合理，足够存储和加载多个 TS 文件的数据，以便在衔接处无缝播放。

需要注意的是，HLS 的分片时长（通过 `-hls_time` 参数设置）也会影响 TS 文件之间的衔接效果。较短的分片时长可以提供更精确的衔接点，但也会增加播放列表（M3U8 文件）的大小和索引的复杂性。

综上所述，确保相邻 TS 文件之间的时间戳连续、PTS 和 DTS 一致，并适当选择衔接点附近的 I 帧，可以实现较为平滑的 TS 文件衔接和连续播放。


# Docker安装srs4
<span style="color: red;">**HLS要求RTMP流的编码为h.264+aac/mp3，否则会自动禁用HLS，会出现RTMP流能看HLS流不能看（或者看到的HLS是之前的流）。**</span>[HLS分发文档](https://ossrs.net/lts/zh-cn/docs/v4/doc/delivery-hls)

查看SRS版本：`./objs/srs -v`

###  srs4配置文本路径

容器内配置文件路径：`/usr/local/srs/conf`中的`docker.conf`文件,电脑端使用OBS推流，使用VLC观看延时**3秒**左右。

### 记录视频回放DVR设置
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230620215608.png)

### srs4低延时配置
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230620192456.png)

基于官方创建示例（此版本时间不是东八区当地时间）：
```sh
docker run --name srs4-v2 -itd -p 1935:1935 -p 1985:1985 -p 8080:8080 --restart always -v C:\Users\keke\dev\Raspberry-Pi\conf:/usr/local/srs/conf registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4 ./objs/srs -c conf/docker.conf

docker run --name srs4-v1 -itd -p 1935:1935 -p 1985:1985 -p 8080:8080 --restart always \
    registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4 ./objs/srs -c conf/docker.conf
```



### 创建SRS4容器服务器


第一步：创建启动一个基于镜像`registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4`的临时容器。
第二步：创建成功后将容器中的`/usr/local/srs/conf`目录复制到宿主机。`docker cp `命令只能在运行状态的容器内部和宿主机之间进行复制。如果容器已经停止，你需要先将其启动，然后再执行 `docker cp `命令。
```sh
#docker cp <容器名称或ID>:<容器内目录路径> <宿主机目录路径>

docker cp srs4-v1:/usr/local/srs/conf ./
```
第三步：修改docker.conf文件，可以使用下面的内容直接替换
第四步:基于Dockerfile构建镜像
第五步：创建一个真正运行的srs容器服务

windwos系统下bat创建SRS4脚本：
```bat
@echo off
setlocal

docker run -itd --name srs4-cow registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4

docker cp srs4-cow:/usr/local/srs/conf ./

docker build -t srs4:v1 .

set "VIDEO_DIR=video"
if not exist "%VIDEO_DIR%" mkdir "%VIDEO_DIR%"

rem 获取当前脚本的绝对路径
for %%I in ("%~dp0.") do set "SCRIPT_PATH=%%~fI"

docker run --name srs4-v1 -itd -p 1935:1935 -p 1985:1985 -p 8080:8080 --restart always -v %SCRIPT_PATH%/conf:/usr/local/srs/conf -v %SCRIPT_PATH%\video:/usr/local/srs/video srs4:v1 ./objs/srs -c conf/docker.conf

docker stop srs4-cow

docker rm srs4-cow
endlocal
```

<span style="color: red;">**推荐**</span>基于`registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4`构建一个东八区当地时间镜像：

**Dockerfile文件：**
```Dockerfile
FROM registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4

RUN sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/mirrors.ustc.edu.cn\/ubuntu\//g' /etc/apt/sources.list
### 设置上海时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN apt-get update && apt-get install -y tzdata

WORKDIR /usr/local/srs
COPY . .

CMD ["./objs/srs" , "-c" , "conf/docker.conf"]
```

```sh
#打包镜像
docker build -t srs4:v1 .

#windwos将录像目录与宿主机绑定、文件系统同宿主机绑定（推荐）
docker run --name srs4-v2 -itd -p 1935:1935 -p 1985:1985 -p 8080:8080 --restart always -v C:\Users\keke\dev\Raspberry-Pi\conf:/usr/local/srs/conf -v C:\Users\keke\dev\Raspberry-Pi\srs\video:/usr/local/srs/video srs4:v1 ./objs/srs -c conf/docker.conf

#树莓派安装（推荐）
docker run --name srs4-v1 -itd -p 1935:1935 -p 1985:1985 -p 8080:8080 --restart always -v $(pwd)/conf:/usr/local/srs/conf -v $(pwd)/video:/usr/local/srs/video srs4:v1 ./objs/srs -c conf/docker.conf

#创建容器，使用默认配置（不推荐）
docker run --name srs4-v2 -itd -p 1935:1935 -p 1985:1985 -p 8080:8080 --restart always srs4:v1 ./objs/srs -c conf/docker.conf


```




#### docker.conf配置：
```Dockerfile
# docker config for srs.
# @see full.conf for detail config.

listen              1935;
max_connections     1000;
# For docker, please use docker logs to manage the logs of SRS.
# See https://docs.docker.com/config/containers/logging/
srs_log_tank        console;
daemon              off;
http_api {
    enabled         on;
    listen          1985;
}
http_server {
    enabled         on;
    listen          8080;
    dir             ./objs/nginx/html;
}
rtc_server {
    enabled on;
    listen 8000;
    # @see https://ossrs.net/lts/zh-cn/docs/v4/doc/webrtc#config-candidate
    candidate $CANDIDATE;
}
vhost __defaultVhost__ {
    #配置记录视频 按vhost/app和年月分目录，流名称、日和时间作为文件名
    dvr {
        enabled      on;
#         dvr_path     /usr/local/srs/video/[app]/[2006]/[01]/[stream]-[02]-[15].[04].[05].[999].mp4;#按vhost/app和年月分目录，流名称、日和时间作为文件名
        dvr_path     /usr/local/srs/video/[app]/[2006]/[01]/[stream]-[02]-[15].[04].[05].mp4;
        dvr_plan     segment;# DVR 计划，可以是 session（会话结束时重新编写 flv/mp4），或者是 segment（当 flv 时长超过指定的 dvr_duration 时重新编写）
        dvr_duration    3600; #DVR 文件时长，单位为秒，超过指定时长将重新编写
        dvr_wait_keyframe       on;# 是否等待关键帧才重新编写 segment，如果关闭，则超过时长就重新编写，如果开启，则等待关键帧后再重新编写
    }
    #降低延时配置
    tcp_nodelay     on;
    min_latency     on;
    play {
        #on就会马上播放，off就低延迟
        gop_cache       off;
        queue_length    10;
        mw_latency      100;
    }
    publish {
        mr off;
    }

    hls {
        enabled         on;
        hls_path        ./objs/nginx/html;
        hls_fragment    2;
        hls_window      60;
    }
    http_remux {
        enabled     on;
        mount       [vhost]/[app]/[stream].flv;
    }
    rtc {
        enabled     on;
        # @see https://ossrs.net/lts/zh-cn/docs/v4/doc/webrtc#rtmp-to-rtc
        rtmp_to_rtc on;
        # @see https://ossrs.net/lts/zh-cn/docs/v4/doc/webrtc#rtc-to-rtmp
        rtc_to_rtmp on;
    }
}

```

## dvr各字段含义：
```nginx
vhost your_vhost {
    dvr {
        enabled         on;                          # 是否启用 DVR 功能，默认为 off
        dvr_apply       all;                         # DVR 应用的过滤器，可以是 all（应用到所有应用的所有流），或者是 <app>/<stream>（应用到指定应用的指定流）
        dvr_plan        session;                     # DVR 计划，可以是 session（会话结束时重新编写 flv/mp4），或者是 segment（当 flv 时长超过指定的 dvr_duration 时重新编写）
        dvr_path        ./objs/nginx/html/[app]/[stream].[timestamp].flv;    # DVR 输出路径，支持使用变量生成文件名
        dvr_duration    30;                           # DVR 文件时长，单位为秒，超过指定时长将重新编写
        dvr_wait_keyframe       on;                    # 是否等待关键帧才重新编写 segment，如果关闭，则超过时长就重新编写，如果开启，则等待关键帧后再重新编写
        time_jitter             full;                  # 时间抖动算法，可以是 full（完全保证流从零开始并且时间递增），或者是 zero（仅保证流从零开始，忽略时间抖动），或者是 off（禁用时间抖动算法）
    }
}


```
# 使用ffmpeg推流
推流树莓派sci摄像头
```sh
#推流本地视频
ffmpeg -re -i test.mp4 -c copy -f flv rtmp://192.168.1.107:1935/live

#推流摄像头
ffmpeg -f video4linux2 -i /dev/video0 -f flv rtmp://192.168.1.107:1935/live/test

ffmpeg -i /dev/video0 -s 640x360 -vcodec libx264 -max_delay 100 -r 20 -b:v 1000k -b:a 128k -f flv rtmp://192.168.1.107:1935/live/test

ffmpeg -f video4linux2 -framerate 30 -video_size 320x240 -i /dev/video0 -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -video_size 320x240 -threads 0 -f flv rtmp://192.168.1.107:1935/live/test

#保存推流视频
ffmpeg -i rtmp://192.168.1.107:1935/live -c copy 文件名.flv
```


```sh
ffmpeg -fflags nobuffer -flags low_delay -strict experimental -i /dev/video0 -s 640x360 -vcodec libx264 -preset ultrafast -tune zerolatency -max_delay 100 -r 20 -b:v 1000k -b:a 128k -f flv rtmp://192.168.1.107:1935/live/test

#禁用音频降低延时
ffmpeg -fflags nobuffer -flags low_delay -strict experimental -i /dev/video0 -s 640x360 -vcodec libx264 -preset ultrafast -tune zerolatency -max_delay 100 -r 20 -b:v 1000k -an -f flv rtmp://192.168.1.107:1935/live/test
```

- -fflags nobuffer：禁用输入缓冲以减少延迟。
- -flags low_delay：启用低延迟模式。
- -strict experimental：启用实验性功能以支持 -flags low_delay。
- -preset ultrafast：使用 ultrafast 预设来最大限度地减少编码延迟。
- -tune zerolatency：启用零延迟调优选项。
- -max_delay 100：设置最大延迟时间为 100 毫秒。
- -r 20：设置输出帧率为 20 帧/秒。
- -b:v 1000k：设置视频比特率为 1000 kbps。
- -b:a 128k：设置音频比特率为 128 kbps。

<span style="color: red;">**该推流延时5秒左右（推荐搭配DVR一起使用）**</span>


```sh
ffmpeg -fflags nobuffer -flags low_delay -strict experimental -i /dev/video0 -s 640x360 -vcodec libx264 -preset ultrafast -tune zerolatency -max_delay 100 -r 20 -b:v 2000k -g 10 -x264opts no-mbtree -an -f flv rtmp://192.168.1.106:1935/live/test
```

推流同时保存视频，此种视频流srs服务端DVR无法保存视频
```sh
ffmpeg -fflags nobuffer -flags low_delay -strict experimental -i /dev/video0 -s 640x360 -vcodec libx264 -preset ultrafast -tune zerolatency -max_delay 100 -r 20 -b:v 2000k -an -f segment -segment_time 60 -segment_format mp4 output_%03d.mp4 -f flv rtmp://192.168.1.106:1935/live/test
```
在上述命令中，我们使用了 -f segment 参数来指定输出格式为分段模式，-segment_time 60 参数表示每个分段的时间间隔为 60 秒，-segment_format mp4 参数指定分段文件的格式为 MP4。output_%03d.mp4 中的 %03d 表示输出文件名的格式，其中 %03d 将被自动递增的数字替换，以确保每个分段文件的唯一性。

# Docker安装nginx、rtmp实现推流

- 容器= 进程， 有且仅有一个前台能持续运行的进程
- nginx 默认是后台守护进程的形式运行， nginx -g "daemon off;" 以前台形式持续运行。

分别将`nginx-1.24.0.tar.gz`、`nginx-rtmp-module-master.zip`、`nginx.conf`、`Dockerfile`上传到目录中，[下载VLC播放器](https://www.videolan.org/vlc/index.zh_CN.html)、PotPlayer

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230426124348.png)
```sh
#构建镜像
docker build -t nginx/rtmp .
#构建容器
docker run -itd --name os1 -p 9500:80 -p 1935:1935 -v /var/www/rtmp/nginx.conf:/usr/local/nginx/conf/nginx.conf --restart=always nginx/rtmp
#推流测试
ffmpeg -re -i test.mp4 -c copy -f flv rtmp://192.168.1.107:1935/live
```
![VLC播放器](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230426124615.png)

Dockerfile文件内容：
```Dockerfile
FROM debian:bullseye-slim

EXPOSE 1935
EXPOSE 80

RUN sed -i 's/deb.debian.org/mirrors.tencent.com/g' /etc/apt/sources.list

RUN mkdir -p /var/www/html/hls
#设置时区
ENV TZ=Asia/Shanghai
RUN apt-get update \
    && apt-get install build-essential libpcre3 libpcre3-dev libssl-dev wget unzip -y

#下载安装
WORKDIR /usr/local/src
RUN wget http://nginx.org/download/nginx-1.24.0.tar.gz
RUN wget https://github.com/arut/nginx-rtmp-module/archive/master.zip
RUN unzip master.zip
RUN tar -zxvf nginx-1.24.0.tar.gz

#从目录复制安装
#ADD nginx-1.24.0.tar.gz /usr/local/src
#ADD nginx-rtmp-module-master.zip  /usr/local/src
#WORKDIR /usr/local/src
#RUN unzip nginx-rtmp-module-master.zip

WORKDIR /usr/local/src/nginx-1.24.0

RUN ./configure \
    --without-http_gzip_module\
    --with-http_ssl_module \
    --add-module=/usr/local/src/nginx-rtmp-module-master && make && make install

WORKDIR /usr/local/nginx/sbin
CMD ["./nginx","-g","daemon off;"]
```

# Nginx搭建RTMP-HLS视频直播服务器m3u8直播

1. 在rtmp配置中增加hls切片设置
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230518182457.png)

```nginx
rtmp {
    server {
        listen 1935;
        chunk_size 4096;
        application live {
            live on;
            hls on;
            hls_path /var/www/html/hls;   #切片存放位置
            hls_fragment 5s;        
            hls_playlist_length 15s;
            hls_continuous on; 
            hls_cleanup on;
            hls_nested on;
           }
        }
    }
```

2. 新增m3u8播放
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230518182545.png)
```nginx
        location /hls {
           types {
            application/vnd.apple.mpegurl m3u8;
            video/mp2ts ts;
           }
           root /var/www/html/;
           add_header Cache-Control no-cache;
           add_header Access-Control-Allow-Origin *;
        }
```

3.m3u8播放地址
```
http://192.168.1.106/hls/index.m3u8
```


# m3u8在线测试源
```
http://playertest.longtailvideo.com/adaptive/bipbop/gear4/prog_index.m3u8
```

# 安装MJPG-Streamer

<span style="color: red;">前提：`sudo raspi-config`开启摄像头</span>

[mjpg-streamer下载地址](https://github.com/jacksonliam/mjpg-streamer)


下载解压成功后进入文件夹`$(pwd)/mjpg-streamer-master/mjpg-streamer-experimental`编译：

```
sudo apt-get install libjpeg8-dev -y
```

报错提示：
```sh
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Package libjpeg8-dev is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source
However the following packages replace it:
  libjpeg62-turbo-dev:armhf libjpeg62-turbo-dev

E: Package 'libjpeg8-dev' has no installation candidate
```

安装`libjpeg8-dev`失败，这可能是因为该软件包已被废弃或不包含在你配置的软件包仓库中。改用下面的安装`libjpeg62-turbo-dev:armhf`
```sh
sudo apt-get install libjpeg62-turbo-dev:armhf

sudo apt-get install gcc g++ -y
sudo apt-get install cmake -y
sudo apt-get install imagemagick -y
sudo apt-get install libjpeg-dev -y

make
sudo make install
```

开启stream服务器：
```
/usr/local/bin/mjpg_streamer -i "/usr/local/lib/mjpg-streamer/input_uvc.so -n -f 30 -r 1280x720" -o "/usr/local/lib/mjpg-streamer/output_http.so -p 8081 -w /usr/local/share/mjpg-streamer/www"
```
-p命令指定端口
启动成功：
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230624040924.png)


浏览器输入以下地址访问：
```
http://192.168.1.107:8081/?action=stream
```

# libcamera-vid参数
`libcamera-vid` 是用于在树莓派上捕捉视频的命令行工具。下面是 `libcamera-vid` 命令的各个参数的详细解释：

- `--level`：指定视频编码的级别。可选值为 1.0、1.1、1.2、1.3、2.0、2.1、2.2、3.0、3.1、3.2、4.0、4.1、4.2、5.0、5.1、5.2、6.0、6.1、6.2、自动（auto）。
- `--framerate`：指定视频的帧率。
- `--width`：指定视频的宽度。
- `--height`：指定视频的高度。
- `--save-pts`：保存视频帧的时间戳到指定的文件。
- `-o, --output`：指定输出视频文件的路径和文件名。（-o -: 指定输出到标准输出（stdout），而不是写入文件。- 表示标准输出。）标准输出流展示、管道输出给软件
- `-t, --timeout`：指定视频的持续时间，单位为毫秒。
- `--denoise`：指定视频降噪的级别。可选值为 auto、off、low、medium、high。
- `-n, --no-display`：禁止显示视频捕捉的预览图像。

这些参数可以根据您的需求进行调整，以获得所需的视频捕捉效果。您可以通过运行 `libcamera-vid --help` 命令来获取更详细的帮助文档和命令选项列表。

标准输出和管道输出有以下区别：

1. 标准输出（stdout）：标准输出是程序默认的输出目标。当程序将输出发送到标准输出时，输出内容会直接显示在终端窗口上。标准输出通常用于向用户显示程序的结果或信息。

2. 管道输出（Pipe）：管道输出是一种将一个程序的输出连接到另一个程序的输入的方法。通过使用管道符号 `|`，可以将一个程序的输出直接传递给另一个程序，作为后者的输入。这样可以实现多个程序之间的数据传递和处理。

区别在于输出的目标和用途：

- 标准输出主要用于直接显示程序的输出内容在终端窗口上，以供用户查看和交互。
- 管道输出主要用于将一个程序的输出作为另一个程序的输入进行处理，实现程序之间的数据传递和协作。

在命令行中，可以使用重定向符号 `>` 将标准输出重定向到文件中，从而将输出保存到文件中而非显示在终端窗口上。而管道符号 `|` 则用于将一个程序的输出传递给另一个程序，实现数据的流动和处理。


# Go开发MJPG-Streamer流媒体服务器

MJPG-Streamer是一个基于HTTP协议的流媒体服务器，它使用MJPEG（Motion JPEG）格式来传输视频流。以下是MJPG-Streamer的基本协议规格：

1. HTTP请求：客户端通过HTTP GET请求来获取视频流数据。请求的URL通常包含服务器的IP地址、端口号和特定的路径。

2. 响应头：服务器会返回HTTP响应头，其中包含一些常见的响应头字段，如Content-Type、Content-Length和Connection。Content-Type字段通常设置为"multipart/x-mixed-replace"，表示多部分数据替换。Content-Length字段表示响应体的长度。

3. 响应体：响应体是一个由多个JPEG图像帧组成的数据流。每个JPEG图像帧都以0xFFD8作为起始标记（SOI，Start of Image），以0xFFD9作为结束标记（EOI，End of Image）。每个图像帧之间通过分隔符0xFFD8来分隔。

4. 分块传输：MJPEG流使用分块传输（Chunked Transfer）方式进行数据传输。每个图像帧被分成多个分块，每个分块都以十六进制的长度值开头，后面跟着实际的数据。

5. 帧间延迟：由于MJPEG流是一系列的JPEG图像帧，每个帧都是独立的图像，因此可能存在帧间延迟。这意味着客户端接收到的帧可能不是实时的，而是有一定延迟的。

请注意，以上是MJPG-Streamer的基本协议规格，具体的实现细节和配置可能会因不同的版本和设置而有所差异。建议参考MJPG-Streamer的官方文档或用户手册，以获取更详细的协议规格和配置说明。

浏览器输入:`http://192.168.1.106:9091/stream`访问，即可打开。
```go
package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

func main() {
	// 设置HTTP路由
	http.HandleFunc("/stream", streamHandler)

	// 启动HTTP服务器
	err := http.ListenAndServe(":9091", nil)
	if err != nil {
		fmt.Println("Failed to start server:", err)
		return
	}
}

func streamHandler(w http.ResponseWriter, req *http.Request) {
	// 设置响应头
	w.Header().Set("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")

	// 无限循环，持续发送图像流
	for {
		// 读取图像数据
		imageData, err := readImage()
		if err != nil {
			fmt.Println("Failed to read image:", err)
			return
		}

		// 写入分隔符和图像数据
		fmt.Fprintf(w, "--boundarydonotcross\r\n")
		fmt.Fprintf(w, "Content-Type: image/jpeg\r\n")
		fmt.Fprintf(w, "Content-Length: %d\r\n\r\n", len(imageData))
		w.Write(imageData)

		// 强制刷新缓冲区，将数据发送到客户端
		flusher, ok := w.(http.Flusher)
		if !ok {
			fmt.Println("Flusher not supported")
			return
		}
		flusher.Flush()

		// 暂停一段时间
		time.Sleep(100 * time.Millisecond)
	}
}

// 读取图像数据（示例函数，需要根据实际情况实现）
func readImage() ([]byte, error) {
	// 从文件系统中打开图像文件
	file, err := os.Open("test.jpg")
	if err != nil {
		return nil, err
	}
	defer file.Close()

	// 读取图像数据到字节切片
	imageData, err := ioutil.ReadAll(file)
	if err != nil {
		return nil, err
	}

	return imageData, nil
}

```


# 以下是使用 Go 语言封装一个 IP 数据报的示例代码：

```go
package main

import (
	"fmt"
	"log"
	"net"
)

func main() {
	// 目标 IP 地址和端口
	destIP := net.ParseIP("192.168.1.100")
	destPort := 8080

	// 源 IP 地址
	srcIP := net.ParseIP("192.168.1.103")

	// 创建 IP 数据报
	ip := &net.IPHeader{
		Version:  4,              // IPv4
		Len:      20,             // IP 头部长度
		TotalLen: 20 + 8,         // IP 数据报总长度
		TTL:      64,             // 生存时间
		Protocol: net.IPProtocolUDP, // 上层协议为 UDP
		Src:      srcIP.To4(),    // 源 IP 地址
		Dst:      destIP.To4(),   // 目标 IP 地址
	}

	// 封装 UDP 数据报
	udp := &net.UDPHeader{
		SrcPort: 12345, // 源端口号
		DstPort: uint16(destPort), // 目标端口号
		Len:     8,     // UDP 头部长度
	}

	// 创建连接
	conn, err := net.DialIP("ip4:udp", nil, &net.IPAddr{IP: destIP})
	if err != nil {
		log.Fatal("Error creating connection:", err)
	}
	defer conn.Close()

	// 构建 IP 数据报头部字节流
	ipBytes, err := ip.Marshal()
	if err != nil {
		log.Fatal("Error marshaling IP header:", err)
	}

	// 构建 UDP 数据报头部字节流
	udpBytes, err := udp.Marshal()
	if err != nil {
		log.Fatal("Error marshaling UDP header:", err)
	}

	// 构建数据报
	packet := append(ipBytes, udpBytes...)

	// 发送数据报
	_, err = conn.Write(packet)
	if err != nil {
		log.Fatal("Error sending packet:", err)
	}

	fmt.Println("Packet sent")
}
```

上述代码创建了一个 IP 数据报，并使用 UDP 协议封装了一个 UDP 数据报。然后，它使用 `DialIP` 建立一个 IP 层连接，并将封装后的数据报发送到目标 IP 地址和端口。请注意，源 IP 地址和目标 IP 地址可以根据实际情况进行修改。

该示例仅封装了 IP 数据报和 UDP 数据报的头部信息，并发送了一个空的 UDP 数据报。实际应用中，您可以根据需要修改数据报的内容和长度。


# 在 Debian 系统中，有几种方式可以设置开机启动：

1. 使用 `/etc/init.d` 脚本：
   在 `/etc/init.d` 目录中创建启动脚本，并使用 `update-rc.d` 命令将其添加到启动项中。这是传统的方法，适用于较早的 Debian 版本。

2. 使用 `systemd`：
   在较新的 Debian 版本中，使用 `systemd` 作为默认的 init 系统。你可以创建一个 `*.service` 文件来描述你的服务，并使用 `systemctl` 命令管理服务的启动和停止。`systemd` 提供了更强大和灵活的服务管理功能。

下面是使用 `systemd` 设置开机启动的示例步骤：

1. 创建一个 `*.service` 文件，例如 `myservice.service`，并将其放置在 `/etc/systemd/system` 目录中。示例文件内容如下：

   ```
   [Unit]
   Description=My Service
   After=network.target

   [Service]
   ExecStart=/path/to/my-service-executable
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   将 `ExecStart` 替换为你的服务实际的可执行文件路径。

2. 运行以下命令以重新加载 `systemd` 配置：

   ```
   sudo systemctl daemon-reload
   ```

3. 启用服务以在启动时自动启动：

   ```
   sudo systemctl enable myservice
   ```

4. 启动服务：

   ```
   sudo systemctl start myservice
   ```

现在，你的服务将在系统启动时自动启动。你还可以使用 `systemctl` 命令来停止、重启或禁用服务。

请注意，如果你使用较旧的 Debian 版本，可能仍需要使用 `/etc/init.d` 脚本方法进行设置。对于较新的 Debian 版本，请优先考虑使用 `systemd` 方法。



# 文章内跳转

- [第一节](#section-1)
- [第二节](#section-2)

## 第一节 {#section-1}

这是第一节的内容。

## 第二节 {#section-2}
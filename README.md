# 树莓派（Raspberry Pi）学习资料总结
>前言：写这份总结目的是树莓派吃灰几年一直运行docker在家当作开发测试的数据库使用，导致之前买的硬件都没有得到充分的利用，再加上以前零零碎碎写的资料不完整、包括开发的Python脚本丢失，比如小车的L298N电机驱动板之前踩过不少坑当时也没能留下资料，包括接线图也没保存。所以决定对这些资料进行重新整理总结汇总，以便以后查看。

**开发板：树莓派3b（Raspberry Pi 3b）**
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

# 树莓派更换国内源

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
```sh
sudo docker run --name mysql-v1 -p 3306:3306 --restart always -v /var/www/MySQL/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=xCl5QUb9ES2YfkvX -d mysql:8.0
sudo docker run --name nginx1 --restart always -p 80:80 -v /var/www/html:/usr/share/nginx/html -v /var/www/nginx:/etc/nginx/conf.d -d nginx
sudo docker run --name php1 --restart always -p 9000:9000 -v /var/www/html:/var/www/html -d php:8.1.18-fpm
sudo docker run -d --name redis-1 --restart always -p 6379:6379 redis

#运行 portainer
sudo docker run -d -p 10000:9000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
```

# 安装pi-dashboard

https://github.com/nxez/pi-dashboard

```
#创建bridge网络
docker network create pi-dashboard-net 

#创建nginx
sudo docker run --name nginx1 --network pi-dashboard-net --network-alias pi-dashboard-nginx --restart always -p 80:80 -v /var/www/html:/usr/share/nginx/html -v /var/www/nginx:/etc/nginx/conf.d -d nginx
#创建php
sudo docker run --name php1 --network pi-dashboard-net --network-alias pi-dashboard-php --restart always -p 9000:9000 -v /var/www/html:/var/www/html -d php:8.1.18-fpm

#将nginx移除mynet局域网络
docker network disconnect 创建的bridge 对应的network-alias

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
- [x] **apt-get安装方式：** Raspberry Pi OS 64 位系统下：`sudo apt-get install supervisor`，通过这种方式安装后，系统自动设置为开机启动。**此种安装方法会变更系统的python3绑定软连接******
- [x] **pip安装方式（推荐）：** Raspberry Pi OS 64 位系统下，桌面版有pip，lite版本没有pip需要自己安装

1. pip安装supervisor
```
sudo pip install  supervisor
```
2. 创建文件夹并上传配置文件到对应的文件夹，配置文件也可以通过命令行生成
/etc/supervisor
/etc/supervisor/conf.d

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230421173449.png)


3. 启动supervisord
```
sudo supervisord -c /etc/supervisor/supervisord.conf
```
4. 设置开机自启动supervisord
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230421173241.png)


## Supervisord配置Syncthing

Syncthing文档[Using Supervisord](https://docs.syncthing.net/users/autostart.html?highlight=home#using-supervisord) 地址

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230421131519.png)

`/etc/supervisor/conf.d`目录中创建`syncthing.conf`配置文件，配置参考如下：

```conf
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

## supervisorctl常用操作命令

```sh
supervisorctl reload            #重启Supervisord
supervisorctl start syncthing   #启动Supervisord
supervisorctl status syncthing  #检查Supervisord状态
supervisorctl tail syncthing    #检查Supervisord日志
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

# docker安装nginx、rtmp实现推流

- 容器= 进程， 有且仅有一个前台能持续运行的进程
- nginx 默认是后台守护进程的形式运行， nginx -g "daemon off;" 以前台形式持续运行。

分别将`nginx-1.24.0.tar.gz`、`nginx-rtmp-module-master.zip`、`nginx.conf`、`Dockerfile`上传到目录中，[下载VLC播放器](https://www.videolan.org/vlc/index.zh_CN.html)、PotPlayer

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230426124348.png)
```
#构建镜像
docker build -t nginx/rtmp .
#构建容器
docker run -itd --name os1 -p 9500:80 -p 1935:1935 -v /var/www/rtmp/nginx.conf:/usr/local/nginx/conf/nginx.conf --restart=always nginx/rtmp
#推流测试
ffmpeg -re -i test.mp4 -c copy -f flv rtmp://192.168.1.107:1935/live
```
![VLC播放器](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230426124615.png)

Dockerfile文件内容：
```sh
FROM debian:stable
EXPOSE 1935
EXPOSE 80
RUN  sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN  apt-get update
RUN  apt-get install build-essential libpcre3 libpcre3-dev libssl-dev unzip -y
#RUN wget http://nginx.org/download/nginx-1.24.0.tar.gz
#RUN wget https://github.com/arut/nginx-rtmp-module/archive/master.zip
ADD nginx-1.24.0.tar.gz /usr/local/src
ADD nginx-rtmp-module-master.zip  /usr/local/src
WORKDIR /usr/local/src
RUN unzip nginx-rtmp-module-master.zip
WORKDIR /usr/local/src
WORKDIR nginx-1.24.0
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

```
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
```
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


查看摄像头
```
ls /dev/video*
```

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230427151415.png)


推流树莓派sci摄像头
```
#推流本地视频
ffmpeg -re -i test.mp4 -c copy -f flv rtmp://192.168.1.107:1935/live

#推流摄像头
ffmpeg -f video4linux2 -i /dev/video0 -f flv rtmp://192.168.1.107:1935/live

ffmpeg -i /dev/video0 -s 640x360 -vcodec libx264 -max_delay 100 -r 20 -b:v 1000k -b:a 128k -f flv rtmp://192.168.1.107:1935/live

ffmpeg -f video4linux2 -framerate 30 -video_size 320x240 -i /dev/video0 -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -video_size 320x240 -threads 0 -f flv rtmp://192.168.1.107:1935/live

#保存推流视频
ffmpeg -i rtmp://192.168.1.107:1935/live -c copy 文件名.flv
```

Streaming Video 直播视频
树莓派输入：
```
libcamera-vid -t 0 --inline --listen -o tcp://0.0.0.0:8888
```
播放器输入
```
tcp/h264://树莓派地址:8888

```

```
vcgencmd get_camera
```
**supported = 1 detected = 0
supported = 0未开启摄像头
detected = 0 表明没有接入摄像头设备**
设置新版摄像头的话detected就为0无法使用ffmpeg推流

# 新版系统设置摄像头

调用`libcamera`命令拍照出现`ERROR: the system appears to be configured for the legacy camera stack
`报错，这是由于在最新的树莓派系统中已经从基于专有 Broadcom GPU 代码的传统相机软件堆栈过渡到基于libcamera的开源堆栈，也就说未来会使用libcamera来替代。libcamera是一个旨在直接从Linux操作系统支持复杂的相机系统的软件库。对于Raspberry Pi，它使我们能够直接从在ARM处理器上运行的开源代码驱动相机系统。

### 解决方法

在`/boot/config.txt`文件中添加`dtoverlay`字段

![根据摄像头配置](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230427121348.png)

#### [dtoverlay字段与摄像头对照表](https://www.raspberrypi.com/documentation/computers/camera_software.html)：如下

![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230427121445.png)
查看PCF8591器件的地址(硬件地址 由器件决定) 


保存视频十秒钟的视频
```
libcamera-vid -t 10000 -o test.h264
```

拍摄照片
```
libcamera-jpeg -o test.jpg
```

# 使用Picamera2拍照
[Picamera2 手册中](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
[Python 绑定libcamera](https://www.raspberrypi.com/documentation/computers/camera_software.html#python-bindings-for-libcamera)
#### 快速拍照并保存，不需要预览
```
from picamera2 import Picamera2, Preview
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()
picam2.capture_file("test.jpg")
```

#### 快速录制视频并保存，不需要预览
```
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.start_and_record_video("test.mp4", duration=5) #视频格式mp4,长度5秒
```

# OSError: libmmal.so: cannot open shared object file: No such file or directory
https://segmentfault.com/a/1190000040009665

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


```
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

# 更换python软连接
https://blog.csdn.net/qq_42887760/article/details/100997264

# 安装使用samba
```
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

配置目录位置：
```
/etc/samba
```

```
各参数意思
[kingston]：分享名称
comment：备注描述
path：共享文件夹目录
writable：是否可写入，不能写入就不能创建文件夹
browseable：是否可以访问浏览
valid user：允许哪个用户访问，这里需要按照指定的账户访问samba服务
```
![Img](https://raw.githubusercontent.com/liutongke/Image-Hosting/master/images/yank-note-picgo-img-20230509191456.png)

`/etc/samba/smb.conf`末尾添加
```
[kingston]
   comment = Kingston
   path = /media/keke/Kingston-A400
   writable = yes
   browseable = yes
   valid user = ubuntu
   available = yes
   create mask = 0777
   directory mask = 0777
   public = yes
   write list = keke
```


sudo mount /dev/sda1 /media/keke/

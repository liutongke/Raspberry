FROM debian:bullseye-slim

WORKDIR /var/www/html

RUN sed -i 's/deb.debian.org/mirrors.tencent.com/g' /etc/apt/sources.list
#设置时区
ENV TZ=Asia/Shanghai
RUN apt-get update \
    && apt-get install libgl1-mesa-glx libglib2.0-0 ffmpeg -y \
    && apt-get install supervisor -y \
    && apt-get install python3 python3-dev python3-pip -y \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install --no-cache-dir Pillow==9.5.0 numpy==1.24.2  opencv-python==4.7.0.72 schedule==1.2.0 natsort==8.3.1

COPY ./monitor_nvr_process_python.conf /etc/supervisor/conf.d/
#看需求是否将运行程序复制进容器中,不复制的话在创建时候需要-v绑定文件夹
COPY . .
#-n 是 supervisord 命令的一个选项，它表示以非守护进程模式（non-daemon mode）运行 supervisord。
CMD [ "supervisord" , "-n", "-c", "/etc/supervisor/supervisord.conf" ]



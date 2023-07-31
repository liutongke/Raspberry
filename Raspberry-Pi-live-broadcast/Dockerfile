FROM debian:bullseye-slim

EXPOSE 1935
EXPOSE 80

RUN sed -i 's/deb.debian.org/mirrors.tencent.com/g' /etc/apt/sources.list

#设置时区
ENV TZ=Asia/Shanghai

RUN mkdir -p /var/www/html/hls

# 安装必要的工具和依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpcre3 \
        libpcre3-dev \
        libssl-dev \
        wget \
        unzip

#网络下载安装
#WORKDIR /usr/local/src
#RUN wget http://nginx.org/download/nginx-1.24.0.tar.gz \
#    && wget https://github.com/arut/nginx-rtmp-module/archive/master.zip \
#    && tar -zxvf nginx-1.24.0.tar.gz \
#    && unzip master.zip

#本地目录复制安装
# 从本地复制 Nginx 和 rtmp 模块压缩文件到镜像中
COPY nginx-1.24.0.tar.gz /usr/local/src/nginx-1.24.0.tar.gz
COPY nginx-rtmp-module-master.zip /usr/local/src/nginx-rtmp-module-master.zip

# 解压 Nginx 和 rtmp 模块压缩文件
WORKDIR /usr/local/src
RUN tar -zxvf nginx-1.24.0.tar.gz \
    && unzip nginx-rtmp-module-master.zip

# 编译和安装 Nginx，同时启用 SSL 和 rtmp 模块
WORKDIR /usr/local/src/nginx-1.24.0
RUN ./configure \
    --without-http_gzip_module \
    --with-http_ssl_module \
    --add-module=/usr/local/src/nginx-rtmp-module-master \
    && make \
    && make install

# 切换到 Nginx 的 sbin 目录，运行 Nginx
WORKDIR /usr/local/nginx/sbin
CMD ["./nginx", "-g", "daemon off;"]
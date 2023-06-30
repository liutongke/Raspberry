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
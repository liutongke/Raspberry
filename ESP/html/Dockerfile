FROM debian:bullseye-slim

EXPOSE 1935
EXPOSE 80

WORKDIR /usr/local/src

RUN  sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN  apt-get update
RUN  apt-get install unzip wget build-essential libpcre3 libpcre3-dev libssl-dev -y

#下载版本
RUN wget http://nginx.org/download/nginx-1.24.0.tar.gz
RUN wget https://github.com/arut/nginx-rtmp-module/archive/master.zip
RUN tar -zxvf nginx-1.24.0.tar.gz
RUN unzip master.zip
WORKDIR /usr/local/src/nginx-1.24.0
#下载版本结束

RUN ./configure \
    --without-http_gzip_module\
    --with-http_ssl_module \
    --add-module=/usr/local/src/nginx-rtmp-module-master && make && make install

WORKDIR /usr/local/nginx/sbin
CMD ["./nginx","-g","daemon off;"]
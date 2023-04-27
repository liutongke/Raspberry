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
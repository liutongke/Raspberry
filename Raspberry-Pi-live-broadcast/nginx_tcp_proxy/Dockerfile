FROM debian:stable
EXPOSE 1935
EXPOSE 80
RUN  sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN  apt-get update
RUN  apt-get install build-essential libpcre3 libpcre3-dev libssl-dev unzip openssl zlib1g zlib1g-dev wget -y
WORKDIR /usr/local/src
RUN wget https://nginx.org/download/nginx-1.24.0.tar.gz
RUN tar -zxvf nginx-1.24.0.tar.gz
WORKDIR /usr/local/src/nginx-1.24.0
RUN ./configure --with-stream
RUN make && make install

WORKDIR /usr/local/nginx/sbin
CMD ["./nginx","-g","daemon off;"]

#docker build -t nginx/tcp/proxy:v1 .
#docker run --name nginx-rtmp-v2 -it -p 9999:80 -p 9998:1935 -v C:\Users\keke\dev\docker\rtmp\html:/var/www/html -v C:\Users\keke\dev\docker\rtmp\html\nginx.conf:/usr/local/nginx/conf/nginx.conf e21004c6c240 /bin/bash

#wget https://nginx.org/download/nginx-1.24.0.tar.gz
#./configure --with-stream
#make
#make install
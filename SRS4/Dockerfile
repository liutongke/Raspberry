FROM registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4

RUN sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/mirrors.ustc.edu.cn\/ubuntu\//g' /etc/apt/sources.list
### 设置上海时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN apt-get update && apt-get install -y tzdata

WORKDIR /usr/local/srs
COPY . .

CMD ["./objs/srs" , "-c" , "conf/docker.conf"]

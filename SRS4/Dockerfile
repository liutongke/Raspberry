FROM registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4

# 使用 USTC 的软件源
RUN sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/mirrors.ustc.edu.cn\/ubuntu\//g' /etc/apt/sources.list

# 设置上海时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 安装 tzdata 包，用于配置时区
RUN apt-get update && apt-get install -y tzdata

# 设置工作目录
WORKDIR /usr/local/srs

# 将当前目录下的所有文件复制到容器的 /usr/local/srs 目录中
COPY . .

# 容器启动时执行的命令
CMD ["./objs/srs", "-c", "conf/docker.conf"]

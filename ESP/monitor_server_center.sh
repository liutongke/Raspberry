#!/bin/bash

# 构建Docker镜像
docker build -t my-monitor-server-center-app .

# 运行Docker容器
docker run --name my-monitor-server-center -it -p 9090:9090/udp my-monitor-server-center-app

# 创建监控推流容器
# 注意：需要确保当前目录下存在 monitor_server_center.py、config.py 和 byte_stream.py 文件
#docker run --name monitor-push-container -v "$(pwd)/monitor_server_center.py:/var/www/html/monitor_server_center.py" -v "$(pwd)/config.py:/var/www/html/config.py" -v "$(pwd)/byte_stream.py:/var/www/html/byte_stream.py" -d my-monitor-server-center-app

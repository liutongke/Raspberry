docker build -t my-monitor-server-center-app .
docker run --name my-monitor-server-center -it -p 9090:9090/udp my-monitor-server-center-app
rem 创建监控推流容器，需要文件monitor_server_center.py、config.py、byte_stream.py
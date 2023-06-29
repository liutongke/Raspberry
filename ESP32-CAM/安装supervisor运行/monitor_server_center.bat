docker build -t monitor-server-center-app-supervisord .
docker run --name monitor-server-center-supervisord -it -p 9090:9090/udp -v C:\Users\keke\dev\Raspberry-Pi\ESP:/var/www/html monitor-server-center-app-supervisord
rem 创建监控推流容器，需要文件monitor_server_center.py、config.py、byte_stream.py
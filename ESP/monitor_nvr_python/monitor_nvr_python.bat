docker build -t monitor-nvr-python:v1 .
docker run --name monitor-nvr-python-server -itd -p 9090:9090/udp monitor-nvr-python:v1
rem docker run --name monitor-process-server -it -p 9090:9090/udp -p 6001:6001 -v C:\Users\keke\dev\Raspberry-Pi\ESP\monitor:/var/www/html monitor-process
rem 创建监控推流容器，需要文件monitor_server_center.py、config.py、byte_stream.py
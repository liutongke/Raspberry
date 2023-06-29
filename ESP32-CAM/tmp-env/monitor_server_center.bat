docker build -t tmp-test-can-del .
docker run --name tmp-test-can-del-socket -it -p 6000:6000/udp -p 6001:6001 -v C:\Users\keke\dev\Raspberry-Pi\ESP:/var/www/html tmp-test-can-del
rem 创建监控推流容器，需要文件monitor_server_center.py、config.py、byte_stream.py
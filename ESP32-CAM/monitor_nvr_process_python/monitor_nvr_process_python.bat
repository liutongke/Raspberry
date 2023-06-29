@echo off

set "current_dir=%cd%"
set "data_dir=%current_dir%\data"

REM 检查目录是否存在
if exist "%data_dir%" (
  echo directory already exists: %data_dir%
) else (
  REM 创建目录
  mkdir "%data_dir%"
  echo Create a directory: %data_dir%
)

docker build -t monitor-nvr-process-python:v1 .
docker run --name monitor-nvr-process-python-server -itd -p 9090:9090/udp -v %data_dir%:/var/www/html/data monitor-nvr-process-python:v1
rem docker run --name monitor-process-server -it -p 9090:9090/udp -p 6001:6001 -v C:\Users\keke\dev\Raspberry-Pi\ESP\monitor:/var/www/html monitor-process
rem 创建监控推流容器，需要文件monitor_server_center.py、config.py、byte_stream.py
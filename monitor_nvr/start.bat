@echo off

set "current_dir=%cd%"
set "data_dir=%current_dir%\data"

REM 检查目录是否存在
if exist "%data_dir%" (
  echo 目录已存在: %data_dir%
) else (
  REM 创建目录
  mkdir "%data_dir%"
  echo 创建目录: %data_dir%
)

docker build -t monitor_nvr_go:v2 .
docker run --name monitor_nvr_go_v1 -itd  -p 9090:9090/udp -v %data_dir%:/var/www/html/data monitor_nvr_go:v2
rem docker run --name go-v1 -itd  -p 9090:9090/udp -p 12346:12346 -v C:\Users\keke\dev\Raspberry-Pi\gpio:/var/www/html go-ffmpeg:latest /bin/bash
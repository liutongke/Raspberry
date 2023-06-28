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

docker build -t go_monitor_nvr:v1 -f ./DockerfileTest .
docker run --name go_monitor_nvr_v1 -it  -p 9091:9091 -p 9090:9090/udp -v %current_dir%:/var/www/html/ go_monitor_nvr:v1 /bin/bash
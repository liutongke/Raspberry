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

docker build -t monitor_nvr_go:v1 -f ./DockerfileTest .
docker run --name monitor_nvr_go_v1 -it  -p 12349:12349 -p 9090:9090/udp -v %current_dir%:/var/www/html/ monitor_nvr_go:v1 /bin/bash
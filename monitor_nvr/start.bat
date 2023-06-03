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

docker build -t monitor_nvr_go:v1 .
docker run --name monitor_nvr_go_v1 -itd  -p 12349:12349 -p 9090:9090/udp -v %data_dir%:/var/www/html/data monitor_nvr_go:v1
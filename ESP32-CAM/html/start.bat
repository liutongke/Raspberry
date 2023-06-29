@echo off

docker network create lnmp-net

docker build -t nginx/rtmp:v1 .


SET dirPath=%~dp0

if not exist "%dirPath%\log\" (
    mkdir "%directory%\log"
    echo "log folder created."
) else (
    echo "log folder already exists."
)

docker run -itd -p 9900:80 -p 9901:1935  --network lnmp-net --network-alias lnmp-net --name nginx-rtmp-1 --restart always -v %dirPath%conf/nginx.conf:/usr/local/nginx/conf/nginx.conf -v %dirPath%log:/usr/local/nginx/logs -v %dirPath%:/var/www/html nginx/rtmp:v1
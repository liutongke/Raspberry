set "confDir=%cd%\conf.d"

if not exist "%confDir%" (
    mkdir "%confDir%"
    echo Created conf.d folder.
) else (
    echo conf.d folder already exists.
)

docker run --name nginx-cow -itd nginx:1.25.0-bullseye

rem #docker cp <容器名称或ID>:<容器内目录路径> <宿主机目录路径>
docker cp nginx-cow:/etc/nginx/conf.d/default.conf ./conf.d

set "current_dir=%cd%"

docker run --name player-video-v1 -d -p 80:80 --restart always -v %current_dir%/html:/usr/share/nginx/html -v %current_dir%/conf.d:/etc/nginx/conf.d/  nginx:1.25.0-bullseye

docker stop nginx-cow
docker rm nginx-cow
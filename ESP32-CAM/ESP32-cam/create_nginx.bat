@echo off

setLocal enableDelayedExpansion

for %%D in (conf.d log) do (
    set "dirName=%%D"
    set "dirPath=%cd%\!dirName!"

    if not exist "!dirPath!" (
        mkdir "!dirPath!"
        echo Created !dirName! folder.
    ) else (
        echo !dirName! folder already exists.
    )
)

endLocal

docker run --name nginx-cow -itd nginx:1.25.0-bullseye

rem #docker cp <容器名称或ID>:<容器内目录路径> <宿主机目录路径>
docker cp nginx-cow:/etc/nginx/conf.d/default.conf ./conf.d

set "current_dir=%cd%"

docker run --name esp32-cam-downloads-main.py -d -p 9900:80 --restart always -v %current_dir%:/usr/share/nginx/html -v %current_dir%/conf.d:/etc/nginx/conf.d/  -v %current_dir%/log:/var/log/nginx nginx:1.25.0-bullseye

docker stop nginx-cow
docker rm nginx-cow
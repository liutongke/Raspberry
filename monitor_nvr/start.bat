docker build -t monitor_nvr:v1 .
docker run --name monitor_nvr-v1 -itd  -p 9090:9090/udp monitor_nvr:v1
rem docker run --name go-v1 -itd  -p 9090:9090/udp -p 12346:12346 -v C:\Users\keke\dev\Raspberry-Pi\gpio:/var/www/html go-ffmpeg:latest /bin/bash
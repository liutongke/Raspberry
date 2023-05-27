docker build -t go-ffmpeg .
docker run --name go-v1 -it  -p 9090:9090/udp -p 12346:12346 -v C:\Users\keke\dev\Raspberry-Pi\gpio:/var/www/html go-ffmpeg:latest /bin/bash
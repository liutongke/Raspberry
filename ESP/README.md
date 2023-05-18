ffmpeg -re -i test.mp4 -c copy -f flv rtmp://192.168.1.106:9001/live/123123123

ffmpeg -re -i 2023-05-17-22-37-00.mp4 -c copy -f flv rtmp://192.168.1.106:9001/live
12秒延时

docker run --name nginx-rtmp-v1 -d -p 9001:1935 -p 80:80 --restart always -v C:\Users\keke\dev\docker\rtmp\nginx.conf:
/usr/local/nginx/conf/nginx.conf -v C:\Users\keke\dev\docker\rtmp\html:/var/www/html 3c1127a74924
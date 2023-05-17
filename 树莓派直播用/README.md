/usr/local/nginx/conf/nginx.conf
docker run --name nginx-rtmp-v1 -d -p 9001:1935 -p 80:80 --restart always -v C:\Users\keke\dev\docker\rtmp\nginx.conf:/usr/local/nginx/conf/nginx.conf 3c1127a74924
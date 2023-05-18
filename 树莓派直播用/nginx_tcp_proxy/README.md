nginx设置tcp转发
docker build -t nginx/tcp/proxy:v1 .

docker run --name nginx-rtmp-v2 -it -p 9999:80 -p 9998:1935 -v C:\Users\keke\dev\docker\rtmp\html:/var/www/html -v C:
\Users\keke\dev\docker\rtmp\html\nginx.conf:/usr/local/nginx/conf/nginx.conf e21004c6c240 /bin/bash
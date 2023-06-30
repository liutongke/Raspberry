docker build -t nginx-rtmp-server:v1 -f ./Dockerfile .

set "current_dir=%cd%"
echo %current_dir%

docker run --name nginx-rtmp-v1 -d -p 9001:1935 -p 80:80 --restart always -v %current_dir%/nginx.conf:/usr/local/nginx/conf/nginx.conf nginx-rtmp-server:v1
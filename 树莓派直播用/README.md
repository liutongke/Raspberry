/usr/local/nginx/conf/nginx.conf
docker run --name nginx-rtmp-v1 -d -p 9001:1935 -p 80:80 --restart always -v C:\Users\keke\dev\docker\rtmp\nginx.conf:
/usr/local/nginx/conf/nginx.conf 3c1127a74924

推拉流地址：rtmp://192.168.1.106:9001/live

nginx.conf配置只支持rtmp推拉流

m3u8配置.conf文件新增hls切片m3u8播放，其它设置包括安装不变

m3u8播放地址：http://192.168.1.106/hls/index.m3u8
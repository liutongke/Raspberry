树莓派路径：/var/www/rtmp/nginx.conf<br>
容器路径：/usr/local/nginx/conf/nginx.conf

```shell
docker run --name nginx-rtmp-v1 -d -p 9001:1935 -p 80:80 --restart always -v C:\Users\keke\dev\docker\rtmp\nginx.conf:
/usr/local/nginx/conf/nginx.conf 3c1127a74924
```

推拉流地址：rtmp://192.168.1.106:9001/live/haha

m3u8播放地址：http://192.168.1.106/hls/haha/index.m3u8

srs直播：
docker run --name srs4-v1 -itd -p 1935:1935 -p 1985:1985 -p 8080:8080 --restart always \
    registry.cn-hangzhou.aliyuncs.com/ossrs/srs:4 ./objs/srs -c conf/docker.conf
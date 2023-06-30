树莓派路径：/var/www/rtmp/nginx.conf<br>
容器路径：/usr/local/nginx/conf/nginx.conf

```shell
docker run --name nginx-rtmp-v1 -d -p 9001:1935 -p 80:80 --restart always -v C:\Users\keke\dev\docker\rtmp\nginx.conf:
/usr/local/nginx/conf/nginx.conf 3c1127a74924
```

推拉流地址：rtmp://192.168.1.106:9001/live/haha

m3u8播放地址：http://192.168.1.106/hls/haha/index.m3u8

windwos系统不建议将`/var/www/html/hls`目录与宿主机绑定，因为文件系统转换原因，会导致系统速度减慢，拉流变卡顿
FROM debian:bullseye-slim

WORKDIR /var/www/html

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
#设置时区
ENV TZ=Asia/Shanghai
RUN apt-get update
RUN apt-get install libgl1-mesa-glx libglib2.0-0 ffmpeg -y
RUN apt-get install python3 python3-dev -y
RUN python3 --version
RUN apt-get install python3-pip -y
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install --no-cache-dir Pillow==9.5.0 numpy==1.24.2  opencv-python==4.7.0.72

COPY . .

CMD [ "python3", "./monitor_server_center.py" ]



#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: save_server.py
@time: 2023/5/15 19:16
@version：Python 3.11.2
@title: 
"""
import socket
import cv2
import io
from PIL import Image
import numpy as np
import time
import datetime


class Cam:
    mp4_file = ''

    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.udp_socket.bind(("0.0.0.0", 9090))
        self.file_obj()

    def file_obj(self):
        # 设置视频的编码解码方式avi
        video_type = cv2.VideoWriter_fourcc(*'XVID')  # 视频存储的格式
        # 保存的位置，以及编码解码方式，帧率，视频帧大小
        now_time = datetime.datetime.now()
        time_str = now_time.strftime("%Y-%m-%d-%H-%M-%S")
        print(time_str)
        # str(time.time())
        self.mp4_file = cv2.VideoWriter('%s.avi' % time_str, video_type, 5, (480, 320))
        # mp4_file.release()

    def save_file(self):
        pass

    def main(self):
        while True:
            data, IP = self.udp_socket.recvfrom(100000)

            imgNp = np.array(bytearray(data), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)

            # all the opencv processing is done here
            cv2.imshow('test', img)
            if ord('q') == cv2.waitKey(10):
                exit(0)
            # bytes_stream = io.BytesIO(data)
            # print(bytes_stream)
            # image = Image.open(bytes_stream)
            # print(image)
            # img = np.asarray(image)
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # ESP32采集的是RGB格式，要转换为BGR（opencv的格式）
            # cv2.imshow("ESP32 Capture Image", img)
            ret = self.mp4_file.write(img)
            t = time.gmtime()
            if t[5] == 0:
                print(t[5])
                self.file_obj()


if __name__ == "__main__":
    try:
        Cam().main()
    except KeyboardInterrupt:
        print("bye bye")

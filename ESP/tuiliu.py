#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: tuiliu.py
@time: 2023/5/16 21:58
@version：Python 3.11.2
@title: 
"""
# 本地摄像头推流
import queue
import threading
import cv2
import subprocess as sp
import socket
import cv2
import io
from PIL import Image
import numpy as np
import os


# 保存图片
def save_image(addr, img3):
    saveFile = 'images/' + str(addr) + '.jpg'
    cv2.imwrite(saveFile, img3)  # 保存图像文件


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.bind(("0.0.0.0", 9090))

# 推流地址
rtmpUrl = "rtmp://192.168.1.106:9001/live/esp32cam"

fps = 6  # 设置过大不符合实际帧率会出现撕裂、绿屏、花屏等各种显示异常问题
width = 800
height = 600

# ffmpeg command
command = ['ffmpeg',
           '-y',
           # 推流速度与视频同步
           '-re',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           # 视频宽高需设置一致，否则显示异常
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
           '-i', '-',
           # 使用低延迟的编解码器：选择具有低延迟特性的编解码器可以减少处理过程中的延迟。例如，可以使用H.264编解码器的低延迟配置（比如"ultrafast"或"superfast"）
           # '-c:v', 'libx264',  # 编码压缩
           # 调整GOP（Group of Pictures）大小：GOP是视频编码中一组关键帧和非关键帧的序列。减小GOP大小可以降低延迟，但可能会增加文件大小。您可以通过设置"-g"选项来调整GOP大小
           '-g', '5',
           # 禁用B帧：B帧（双向预测帧）在视频编码中引入了更高的压缩率，但也会增加延迟。通过禁用B帧，可以减少延迟。使用"-bf 0"选项可以禁用B帧
           '-bf', '0',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           rtmpUrl]
i = 0
# 设置管道
p = sp.Popen(command, stdin=sp.PIPE)
while True:
    i += 1
    data, IP = s.recvfrom(100000)

    imgNp = np.array(bytearray(data), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    # 保存图片
    save_image(i, img)
    # 预览显示
    # cv2.imshow('rtmp', img)
    # 管道推流
    p.stdin.write(img.tostring())

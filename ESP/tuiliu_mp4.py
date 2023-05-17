#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: tuiliu_mp4.py
@time: 2023/5/16 23:35
@version：Python 3.11.2
@title: 
"""
# 本地摄像头推流
import queue
import threading
import cv2
import subprocess as sp

# 自行设置,url为推送的服务器地址
rtmpUrl = "rtmp://192.168.1.106:9001/live"
cap = cv2.VideoCapture("test.mp4")

fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# ffmpeg command
command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(width, height),
           '-r', str(fps),
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           rtmpUrl]

# 设置管道
p = sp.Popen(command, stdin=sp.PIPE)
while True:
    ret, frame = cap.read()
    p.stdin.write(frame.tostring())

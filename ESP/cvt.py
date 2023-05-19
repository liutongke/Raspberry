#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: cvt.py
@time: 2023/5/18 20:47
@version：Python 3.11.2
@title: 
"""

import subprocess as sp
import socket
import cv2
import io
from PIL import Image
import numpy as np
import time


class Monitor:
    rtmpUrl = "rtmp://192.168.1.106:9001/live/raspi"  # 推流地址
    fps = 30  # 设置过大不符合实际帧率会出现撕裂、绿屏、花屏等各种显示异常问题
    width = 640
    height = 480

    is_first = False
    gray_background = None

    def __init__(self):
        self.out = None

    def run(self):
        # ffmpeg command
        command = ['ffmpeg',
                   '-y',
                   # 推流速度与视频同步
                   '-re',
                   '-f', 'rawvideo',
                   '-vcodec', 'rawvideo',
                   '-pix_fmt', 'bgr24',
                   # 视频宽高需设置一致，否则显示异常
                   '-s', "{}x{}".format(self.width, self.height),
                   '-r', str(self.fps),
                   '-i', '-',
                   # 使用低延迟的编解码器：选择具有低延迟特性的编解码器可以减少处理过程中的延迟。例如，可以使用H.264编解码器的低延迟配置（比如"ultrafast"或"superfast"）
                   # '-c:v', 'libx264',  # 编码压缩
                   '-b:v', '4M',  # 设置视频编码器和比特率：选择适当的视频编码器（如libx264或libx265）并设置目标比特率。较高的比特率可以提高画质，但会增加带宽需求
                   # 调整GOP（Group of Pictures）大小：GOP是视频编码中一组关键帧和非关键帧的序列。减小GOP大小可以降低延迟，但可能会增加文件大小。您可以通过设置"-g"选项来调整GOP大小
                   '-g', '5',
                   # 禁用B帧：B帧（双向预测帧）在视频编码中引入了更高的压缩率，但也会增加延迟。通过禁用B帧，可以减少延迟。使用"-bf 0"选项可以禁用B帧
                   '-bf', '0',
                   '-pix_fmt', 'yuv420p',
                   '-preset', 'ultrafast',
                   '-f', 'flv',
                   self.rtmpUrl]
        # self.init_save_video()  # 初始化保存视频参数
        i = 0
        p = sp.Popen(command, stdin=sp.PIPE)  # 设置管道

        cap = cv2.VideoCapture(0)

        cap.set(3, 640)  # 摄像头采集图像的宽度320
        cap.set(4, 480)  # 摄像头采集图像的高度240
        cap.set(5, 30)  # 摄像头采集图像的帧率fps为30

        # 查看采集图像的参数
        print(cap.get(3))
        print(cap.get(4))
        print(cap.get(5))

        while True:
            i += 1
            ret, img = cap.read()
            # img = self.decode_stream(data)
            # img = self.water_mark(data)  # 添加水印

            # img = self.decode_stream(data)# 不添加水印直接推流

            # self.save_image(i, data)  # 保存图片

            # cv2.imshow('rtmp', img) # 预览显示
            # self.save_video(img)  # 保存视频

            p.stdin.write(img.tostring())  # 管道推流

    '''
    保存视频
    '''

    def save_video(self, img):
        self.out.write(img)

    '''
    初始化保存视频
    '''

    def init_save_video(self):
        text = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        # 定义输出视频的文件名、编解码器、帧率和分辨率
        output_filename = '%s.mp4' % text

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编解码器，此处使用MP4V
        # fps = 30  # 帧率
        # frame_width = 640  # 视频宽度
        # frame_height = 480  # 视频高度

        # 创建VideoWriter对象
        self.out = cv2.VideoWriter(output_filename, fourcc, self.fps, (self.width, self.height))

    '''
    不加水印直接推流
    '''

    def decode_stream(self, data):
        imgNp = np.array(bytearray(data), dtype=np.uint8)
        return cv2.imdecode(imgNp, -1)

    '''
    给照片增加水印
    '''

    def water_mark(self, data):
        image = Image.open(io.BytesIO(data))
        img = np.asarray(image)
        RGB_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # ESP32采集的是RGB格式，要转换为BGR（opencv的格式）

        # if not self.is_first:
        #     frame = cv2.resize(RGB_img, None, fx=0.5, fy=0.5)  # 可选：调整图像大小
        #     gray_background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
        #     self.gray_background = cv2.GaussianBlur(gray_background, (21, 21), 0)  # 可选：应用高斯模糊
        #     self.is_first = True

        blank_img = np.zeros(shape=(RGB_img.shape[0], RGB_img.shape[1], 3), dtype=np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX

        text = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # 添加水印的文字内容 org：水印放置的横纵坐标，(x坐标，y坐标) width = 800 height = 600
        cv2.putText(blank_img, text=text, org=(420, 580),
                    fontFace=font, fontScale=1,
                    color=(100, 255, 0), thickness=2, lineType=cv2.LINE_4)

        blended = cv2.addWeighted(src1=RGB_img, alpha=0.7,
                                  src2=blank_img, beta=1, gamma=2)
        # self.move_motion(RGB_img, self.gray_background)  # 移动检测
        return blended

    '''
    保存图片
    '''

    def save_image(self, addr, img3):
        saveFile = 'images/' + str(addr) + '.jpg'
        cv2.imwrite(saveFile, img3)  # 保存图像文件


if __name__ == "__main__":
    try:
        Monitor().run()
    except KeyboardInterrupt:
        print("bye bye")

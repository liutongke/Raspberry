#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: monitor_server_center.py
@time: 2023/5/16 21:58
@version：Python 3.11.2
@title: 
"""
# 本地摄像头推流
import subprocess as sp
from PIL import Image
import numpy as np
import byte_stream
import config
import socket
import time
import cv2
import io
import os


class Monitor:
    is_init = {}
    pic_idx = {}

    listen_ip = "0.0.0.0"

    is_first = False
    gray_background = None

    def __init__(self):
        self.cam_param = config.cam_param()
        self.p = {}
        self.out = {}
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        if self.udp_socket.bind((self.listen_ip, config.get_server_port())) is None:
            print("等待客户端接入")

    def run(self):
        while True:
            data, IP = self.udp_socket.recvfrom(100000)

            device_id, payload = byte_stream.decode_payload(data)
            if self.is_init.get(device_id) is None:
                self.init_cam(device_id)

            self.pic_idx[device_id] += 1

            if config.is_open_water_mark():
                img = self.water_mark(payload, device_id)  # 添加水印
            else:
                img = self.decode_stream(data)  # 不添加水印直接推流

            addr = f'{device_id}/' + str(self.pic_idx[device_id]) + '.jpg'
            if config.is_open_save_pic():
                self.save_image(addr, img)  # 保存图片
            # if i <= 320:
            #     addr = f'{s}/' + str(i) + '.jpg'
            #     self.save_image(addr, img)  # 保存图片
            # i += 1
            # if i == 320:
            #     i = 0
            #     s += 1
            # cv2.imshow('rtmp', img) # 预览显示
            if config.is_open_save_video():
                self.save_video(img, device_id)  # 保存视频

            self.p[device_id].stdin.write(img.tobytes())  # 管道推流

    def init_cam(self, device_id):
        # ffmpeg command
        command = ['ffmpeg',
                   '-y',
                   # 推流速度与视频同步
                   '-re',
                   '-f', 'rawvideo',
                   '-vcodec', 'rawvideo',
                   '-pix_fmt', 'bgr24',
                   # 视频宽高需设置一致，否则显示异常
                   '-s', "{}x{}".format(self.cam_param[device_id]["width"], self.cam_param[device_id]["height"]),
                   '-r', str(self.cam_param[device_id]["fps"]),  # 设置过大不符合实际帧率会出现撕裂、绿屏、花屏等各种显示异常问题
                   '-i', '-',
                   # 使用低延迟的编解码器：选择具有低延迟特性的编解码器可以减少处理过程中的延迟。例如，可以使用H.264编解码器的低延迟配置（比如"ultrafast"或"superfast"）
                   # 编码压缩,不使用此编码的话ckplay播放flv出现flv:unsupported codec in video frame:2(code：-1)错误，无法正常播放
                   '-c:v', 'libx264',
                   '-b:v', '2M',  # 设置视频编码器和比特率：选择适当的视频编码器（如libx264或libx265）并设置目标比特率。较高的比特率可以提高画质，但会增加带宽需求
                   # 调整GOP（Group of Pictures）大小：GOP是视频编码中一组关键帧和非关键帧的序列。减小GOP大小可以降低延迟，但可能会增加文件大小。您可以通过设置"-g"选项来调整GOP大小
                   '-g', '5',
                   # 禁用B帧：B帧（双向预测帧）在视频编码中引入了更高的压缩率，但也会增加延迟。通过禁用B帧，可以减少延迟。使用"-bf 0"选项可以禁用B帧
                   '-bf', '0',
                   '-pix_fmt', 'yuv420p',
                   # 该参数控制编码器的速度和质量之间的权衡。较低的预设（如ultrafast）可以提高编码速度，但可能会降低视频质量。较高的预设（如slow）可以提高视频质量，但编码速度较慢。您可以尝试不同的预设选项来平衡编码速度和质量，例如 - presetfast。
                   '-preset', 'ultrafast',
                   '-f', 'flv',
                   self.cam_param[device_id]["rtmp-url"]]
        if config.is_open_save_video():
            self.init_save_video(device_id)  # 初始化保存视频参数

        self.p[device_id] = sp.Popen(command, stdin=sp.PIPE)  # 设置管道
        self.is_init[device_id] = True
        self.pic_idx[device_id] = 0

    '''
    保存视频
    '''

    def save_video(self, img, device_id):
        self.out[device_id].write(img)

    '''
    初始化保存视频
    '''

    def init_save_video(self, device_id):
        filename = "%s_videos" % device_id
        self.mkdir(filename)
        text = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        # 定义输出视频的文件名、编解码器、帧率和分辨率
        output_filename = '%s/%s.mp4' % (filename, text)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编解码器，此处使用MP4V
        # fps = 30  # 帧率
        # frame_width = 640  # 视频宽度
        # frame_height = 480  # 视频高度

        # 创建VideoWriter对象
        self.out[device_id] = cv2.VideoWriter(output_filename, fourcc, self.cam_param[device_id]["fps"],
                                              (self.cam_param[device_id]["width"], self.cam_param[device_id]["height"]))

    '''
    不加水印直接推流
    '''

    def decode_stream(self, data):
        imgNp = np.array(bytearray(data), dtype=np.uint8)
        return cv2.imdecode(imgNp, -1)

    '''
    给照片增加水印
    '''

    def water_mark(self, data, device_id):
        image = Image.open(io.BytesIO(data))
        img = np.asarray(image)
        RGB_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # ESP32采集的是RGB格式，要转换为BGR（opencv的格式）

        # imgNp = np.array(bytearray(data), dtype=np.uint8)
        # RGB_img = cv2.imdecode(imgNp, -1)

        # if not self.is_first:
        #     frame = cv2.resize(RGB_img, None, fx=0.5, fy=0.5)  # 可选：调整图像大小
        #     gray_background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
        #     self.gray_background = cv2.GaussianBlur(gray_background, (21, 21), 0)  # 可选：应用高斯模糊
        #     self.is_first = True

        blank_img = np.zeros(shape=(RGB_img.shape[0], RGB_img.shape[1], 3), dtype=np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX

        text = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        fps_text = f'{device_id} {self.cam_param[device_id]["fps"]}fps'
        # 添加水印的文字内容 org：水印放置的横纵坐标，(x坐标，y坐标) width = 800 height = 600
        cv2.putText(blank_img, text=fps_text, org=(10, 25),
                    fontFace=font, fontScale=1,
                    color=(100, 255, 0), thickness=2, lineType=cv2.LINE_4)
        cv2.putText(blank_img, text=text, org=(420, 580),
                    fontFace=font, fontScale=1,
                    color=(100, 255, 0), thickness=2, lineType=cv2.LINE_4)

        blended = cv2.addWeighted(src1=RGB_img, alpha=0.7,
                                  src2=blank_img, beta=1, gamma=2)
        # self.move_motion(RGB_img, self.gray_background)  # 移动检测
        return blended

    '''
    移动检测
    frame 读取一帧图像
    '''

    def move_motion(self, frame, gray_background, device_id):
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5)  # 可选：调整图像大小
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)  # 可选：应用高斯模糊

        # 计算当前帧与背景帧的差异
        frame_delta = cv2.absdiff(gray_background, gray_frame)
        thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]

        # 执行形态学操作，去除噪声
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 遍历检测到的轮廓
        for contour in contours:
            if cv2.contourArea(contour) < 1000:  # 可选：设置最小轮廓面积
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 显示当前帧
        addr = 'move/' + str(self.pic_idx[device_id]) + '.jpg'
        self.save_image(addr, frame)

    '''
    保存图片
    '''

    def save_image(self, addr, img3):
        # saveFile = 'images/' + str(addr) + '.jpg'
        result = addr.split('/')[0]
        self.mkdir(result)
        cv2.imwrite(addr, img3)  # 保存图像文件

    def mkdir(self, filename):
        if not os.path.exists(filename):  # 判断所在目录下是否有该文件名的文件夹
            os.mkdir(filename)  # 创建多级目录用mkdirs，单击目录mkdir


if __name__ == "__main__":
    try:
        Monitor().run()
    except KeyboardInterrupt:
        print("bye bye")

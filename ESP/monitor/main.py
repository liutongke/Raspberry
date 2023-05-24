#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: process_socket.py
@time: 2023/5/23 18:50
@version：Python 3.11.2
@title: 
"""
import socket
from multiprocessing import Manager, Process, cpu_count
import multiprocessing
import os
import re
import traceback
import tcp_socket, udp_socket, tools
import config
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
import queue_handler


def ffmpeg() -> dict:
    _dict = config.cam_param()
    p = {}
    for key, value in _dict.items():
        # ffmpeg command
        command = ['ffmpeg',
                   '-y',
                   # 推流速度与视频同步
                   '-re',
                   '-f', 'rawvideo',
                   '-vcodec', 'rawvideo',
                   '-pix_fmt', 'bgr24',
                   # 视频宽高需设置一致，否则显示异常
                   '-s', "{}x{}".format(value["width"], value["height"]),
                   '-r', str(value["fps"]),  # 设置过大不符合实际帧率会出现撕裂、绿屏、花屏等各种显示异常问题
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
                   value["rtmp-url"]]

        p[key] = sp.Popen(command, stdin=sp.PIPE)  # 设置管道
    return p


if __name__ == "__main__":
    ffmpeg = ffmpeg()
    queue_dict = {}
    for key, value in ffmpeg.items():
        q = multiprocessing.Queue()  # 储存照片
        consumer_process = Process(target=queue_handler.rtmp_consumer, args=(q, value))
        consumer_process.start()
        queue_dict[key] = q

    manager = Manager()
    shared_dict = manager.dict({})  # 创建共享内存
    # 获取计算机的核心数量
    num_cores = cpu_count()
    print("Number of CPU cores:", num_cores)

    process_udp = Process(target=udp_socket.UdpSocket().udp, args=(shared_dict, queue_dict,))
    process_tcp = Process(target=tcp_socket.TcpSocket().tcp, args=(shared_dict,))

    process_udp.start()
    process_tcp.start()

    process_tcp.join()
    process_udp.join()

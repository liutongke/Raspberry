#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: raspi_send_cam.py
@time: 2023/5/19 12:19
@version：Python 3.11.2
@title: 树莓派通过udp发送照片
"""

import subprocess as sp
import socket
import cv2
import io
from PIL import Image
import numpy as np
import time
from PIL import Image
import io
import byte_stream


def run():
    cap = cv2.VideoCapture(0)

    cap.set(3, 800)  # 摄像头采集图像的宽度320
    cap.set(4, 600)  # 摄像头采集图像的高度240
    # cap.set(5, 30)  # 摄像头采集图像的帧率fps为30

    # 查看采集图像的参数
    print(cap.get(3))
    print(cap.get(4))
    # print(cap.get(5))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    # 获取接收缓冲区大小
    recv_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

    # 获取发送缓冲区大小
    send_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    elapsed_time = 1 / 30
    # 打印接收缓冲区大小和发送缓冲区大小
    print("接收缓冲区大小:", recv_buffer_size)
    print("发送缓冲区大小:", send_buffer_size)
    while True:
        ret, img = cap.read()
        # 将图像转换为JPEG数据流
        _, jpeg_frame = cv2.imencode('.jpg', img)
        jpeg_data = jpeg_frame.tobytes()
        ys_jpeg_data = compress_pic(jpeg_data)
        # print("数据长度：", len(jpeg_data))
        # print("压缩后数据长度：", len(ys_jpeg_data))
        send_data = byte_stream.encode_payload(ys_jpeg_data)

        s.sendto(send_data, ("192.168.1.106", 9090))  # 向服务器发送图像数据
        time.sleep(elapsed_time)


'''
压缩照片
用UDP协议发送时，用sendto函数最大能发送数据的长度为：65535- IP头(20) - UDP头(8)＝65507字节
'''


def compress_pic(image_stream):
    # 假设有一个图像数据流 image_stream
    # 将图像数据流转换为图像对象
    image = Image.open(io.BytesIO(image_stream))

    # 创建一个内存中的字节流缓冲区
    buffer = io.BytesIO()

    # 压缩图像
    image.save(buffer, format='JPEG', quality=80)

    # 获取压缩后的图像数据流
    compressed_image_stream = buffer.getvalue()

    # 关闭图像对象和缓冲区
    image.close()
    buffer.close()

    # 可以在这里使用 compressed_image_stream 进行后续操作
    return compressed_image_stream


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("bye bye")

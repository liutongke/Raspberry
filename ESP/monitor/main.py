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
import pic_handler

if __name__ == "__main__":
    manager = Manager()
    shared_dict = manager.dict({})  # 创建共享内存

    ffmpeg = pic_handler.PicHandler().ffmpeg()

    img_queue_dict = {}
    p_queue_dict = {}

    for device_id, p in ffmpeg.items():
        img_queue = multiprocessing.Queue()  # 储存照片管道
        p_queue = multiprocessing.Queue()  # p推流管道

        rtmp_steam_push_process = Process(target=pic_handler.PicHandler().rtmp_steam_push,
                                          args=(p_queue, shared_dict, img_queue, p))
        img_process = Process(target=queue_handler.save_image,
                              args=(img_queue,))

        rtmp_steam_push_process.start()

        img_process.start()

        img_queue_dict[device_id] = img_queue
        p_queue_dict[device_id] = p_queue

    # 获取计算机的核心数量
    num_cores = cpu_count()
    print("Number of CPU cores:", num_cores)

    process_udp = Process(target=udp_socket.UdpSocket().udp, args=(p_queue_dict,))
    process_tcp = Process(target=tcp_socket.TcpSocket().tcp, args=(shared_dict,))

    process_udp.start()
    process_tcp.start()

    process_tcp.join()
    process_udp.join()

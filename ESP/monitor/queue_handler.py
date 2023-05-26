#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: queue_handler.py
@time: 2023/5/24 4:54
@version：Python 3.11.2
@title: 
"""
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
import tools


def save_video(queue, video_queue, device_id):
    while True:
        item = queue.get()
        video_queue.write(item['img'])


def save_image(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        # saveFile = 'images/' + str(addr) + '.jpg'
        addr = item['addr']
        img3 = item['img']
        # result = addr.split('/')[0]
        tools.mkdirs(tools.get_dir_path(addr))
        cv2.imwrite(addr, img3)  # 保存图像文件

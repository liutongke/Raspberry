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


def rtmp_consumer(queue, p):
    while True:
        item = queue.get()
        # if item is None:
        #     break
        p.stdin.write(item.tobytes())  # 管道推流


def save_image(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        # saveFile = 'images/' + str(addr) + '.jpg'
        addr = item['addr']
        img3 = item['img']
        result = addr.split('/')[0]
        mkdir(result)
        cv2.imwrite(addr, img3)  # 保存图像文件


def mkdir(filename):
    if not os.path.exists(filename):  # 判断所在目录下是否有该文件名的文件夹
        os.mkdir(filename)  # 创建多级目录用mkdirs，单击目录mkdir

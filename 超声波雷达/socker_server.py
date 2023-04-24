#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: socker_server.py
@time: 2023/4/23 20:35
@version：Python 3.11.2
@title: 
"""
import socket  # 导入socket模块
import time  # 导入time模块
import Tools
import radar

ip = '0.0.0.0'
port = 8001
ttl = 10

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (ip, port)
server_socket.bind(address)  # 为服务器绑定一个固定的地址，ip和端口
server_socket.settimeout(ttl)  # 设置一个时间提示，如果10秒钟没接到数据进行提示

while True:
    try:
        now = time.time()  # 获取当前时间
        receive_data, client = server_socket.recvfrom(9000)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))  # 以指定格式显示时间
        d = Tools.json_decode(receive_data)
        radar.radar(d['theta_arr'], d['r'], d['angle'])
    except socket.timeout:
        print("tme out")
        exit()

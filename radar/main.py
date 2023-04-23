#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: main.py
@time: 2023/4/23 20:21
@version：Python 3.11.2
@title: 
"""

import socket
import time
import sg90180 as sg
import HCSR04


class Leida:
    socket_client = ''

    def __init__(self):
        # 定义一个ip协议版本AF_INET，为IPv4；同时也定义一个传输协议（TCP）SOCK_STREAM
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 定义IP地址与端口号
        # 进行连接服务器
        self.socket_client.connect(('192.168.1.105', 8000))

    # 发送消息
    def send(self, send_data):
        while True:
            self.socket_client.send(send_data.encode('utf-8'))  # 将发送的数据进行编码


if __name__ == '__main__':
    sg.sg90_turn(0)
    print("归零")
    time.sleep(1)
    sg.incr()
    sg.decr()

    sg.sg90_turn('stop')
    time.sleep(1)

    sg.clear()  # 清理 在退出时使用
    print("bye bye")
# Leida().send("2244")
# for i in range(1, 5):
#     print(i)
#     Leida().send("i")
#     time.sleep(1)

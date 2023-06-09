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
import Tools


class Leida:
    ip = '192.168.1.105'
    port = 8001
    socket_client = ''

    dict_ = {
        'theta_arr': [],
        'r': [],
        'angle': '',
    }

    def __init__(self):
        # 定义一个ip协议版本AF_INET，为IPv4；同时也定义一个传输协议（TCP）SOCK_STREAM
        # self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 发送消息
    def send(self, send_data):
        self.socket_client.sendto(send_data.encode('utf-8'), (self.ip, self.port))  # 将发送的数据进行编码

    def sg_turn(self, start, stop, step):
        theta_arr = []
        r = []
        for n in range(start, stop, step):
            theta_arr.append(Tools.angle_conversion(n))
            sg.sg90_turn(n)
            distance = HCSR04.launch()
            r.append(300 if distance >= 100 else distance)
            self.dict_['theta_arr'] = theta_arr
            self.dict_['r'] = r
            self.dict_['angle'] = Tools.angle_conversion(n)
            str2 = Tools.json_encode(self.dict_)
            self.send(str2)
            time.sleep(0.1)


if __name__ == '__main__':
    sg.sg90_turn(0)
    print("归零")
    time.sleep(1)

    Leida().sg_turn(0, 180, 1)
    Leida().sg_turn(180, 0, -1)

    sg.sg90_turn('stop')
    time.sleep(1)

    sg.clear()  # 清理 在退出时使用
    print("bye bye")

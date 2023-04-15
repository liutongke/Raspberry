#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: GetLocalIp.py
@time: 2023/4/15 21:59
@version：Python 3.11.2
@title: 获取树莓派ip地址
"""

import socket


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


myAddrIp = get_host_ip()  # 获取本机ip
print(myAddrIp)

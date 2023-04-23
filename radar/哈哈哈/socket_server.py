#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: socket.py
@time: 2023/4/20 22:50
@version：Python 3.11.2
@title: 
"""
# 引入socket库
import socket
import test

# 这是进行定义一个ip协议版本AF_INET（IPv4），定义一个传输TCP协议，SOCK_STREAM
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 定义ip地址与端口号，ip地址就是服务端的ip地址，端口随便定义，但要与客户端脚本一致
ip_port = ('0.0.0.0', 8000)
# 绑定一个端口
sk.bind(ip_port)
# 监听一个端口,这里的数字3是一个常量，表示阻塞3个连接，也就是最大等待数为3
sk.listen(3)
# 接受客户端的数据，并返回两个参数，a为连接信息，b为客户端的ip地址与端口号
a, b = sk.accept()
print(a)
while True:
    data = a.recv(1024)  # 客户端发送的数据存储在recv里，1024指最大接受数据的量
    message = data.decode('utf-8')
    if message == 'bye':
        break
    test.dump(message)
    a.send(message.encode('utf-8'))

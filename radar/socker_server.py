#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: socker_server.py
@time: 2023/4/23 20:35
@version：Python 3.11.2
@title: 
"""
# import socket
# import Tools
#
# # 这是进行定义一个ip协议版本AF_INET（IPv4），定义一个传输TCP协议，SOCK_STREAM
# sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 定义ip地址与端口号，ip地址就是服务端的ip地址，端口随便定义，但要与客户端脚本一致
# ip_port = ('0.0.0.0', 8000)
# # 绑定一个端口
# sk.bind(ip_port)
# # 监听一个端口,这里的数字3是一个常量，表示阻塞3个连接，也就是最大等待数为3
# sk.listen(3)
# # 接受客户端的数据，并返回两个参数，a为连接信息，b为客户端的ip地址与端口号
# a, b = sk.accept()
# print(a)
# while True:
#     data = a.recv(1024)  # 客户端发送的数据存储在recv里，1024指最大接受数据的量
#     message = data.decode('utf-8')
#     if message == 'bye':
#         break
#     print(Tools.json_decode(message))
#     # test.dump(message)
#     # a.send(message.encode('utf-8'))
import socket  # 导入socket模块
import time  # 导入time模块
import Tools
import radar

# server 接收端
# 创建一个套接字socket对象，用于进行通讯
# socket.AF_INET 指明使用INET地址集，进行网间通讯
# socket.SOCK_DGRAM 指明使用数据协议，即使用传输层的udp协议
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ('0.0.0.0', 8001)
server_socket.bind(address)  # 为服务器绑定一个固定的地址，ip和端口
server_socket.settimeout(60)  # 设置一个时间提示，如果10秒钟没接到数据进行提示

while True:
    # 正常情况下接收数据并且显示，如果10秒钟没有接收数据进行提示（打印 "time out"）
    # 当然可以不要这个提示，那样的话把"try:" 以及 "except"后的语句删掉就可以了
    try:
        now = time.time()  # 获取当前时间

        # 接收客户端传来的数据 recvfrom接收客户端的数据，默认是阻塞的，直到有客户端传来数据
        # recvfrom 参数的意义，表示最大能接收多少数据，单位是字节
        # recvfrom返回值说明
        # receive_data表示接受到的传来的数据,是bytes类型
        # client  表示传来数据的客户端的身份信息，客户端的ip和端口，元组
        receive_data, client = server_socket.recvfrom(2024)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))  # 以指定格式显示时间
        # print("来自客户端%s,发送的%s\n" % (client, receive_data))  # 打印接收的内容
        d = Tools.json_decode(receive_data)
        print(d)
        radar.radar(d['theta_arr'], d['r'])
    except socket.timeout:
        print("tme out")
        exit()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: tcp_socket.py
@time: 2023/5/23 21:10
@version：Python 3.11.2
@title: 
"""
import socket
from multiprocessing import Process, cpu_count
import os
import re
import traceback
import tools
import sys


class TcpSocket:
    def handle_tcp_client(self, client_socket, shared_list):
        while True:
            try:
                # 处理客户端连接的逻辑
                data = client_socket.recv(1024)
                # 处理接收到的数据
                # ...
                print(data, data == b'q')
                print(f"tcp接收到数据：{data.decode('utf-8')},{str(data)}")
                # tools.log(f"tcp接收到数据：{data.decode('utf-8')},{str(data)}")
                # 发送响应数据给客户端
                response = "Hello from server"
                client_socket.send(response.encode())
                if data == b'd':
                    print(shared_list)
                if data == b'q':
                    client_socket.close()
                    sys.exit()

            except Exception as e:
                print("tcp接收到处理不了的数据了")
                print(e)
                # 获取异常的详细信息
                traceback_info = traceback.format_exc()
                print(traceback_info)
                client_socket.close()
                sys.exit()

    def tcp(self, shared_list):
        server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置端口号复用，让程序退出端口号立即释放，否则的话在30秒-2分钟之内这个端口是不会被释放的，这是TCP的为了保证传输可靠性的机制。
        server_tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        server_tcp_socket.bind(("0.0.0.0", 6001))
        server_tcp_socket.listen(5)
        if server_tcp_socket.fileno() != -1:
            print("TCP启动成功-prot:6001")
        while True:
            client_socket, addr = server_tcp_socket.accept()
            p = Process(target=self.handle_tcp_client, args=(client_socket, shared_list))
            p.start()

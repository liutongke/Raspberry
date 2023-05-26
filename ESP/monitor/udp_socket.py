#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: udp_socket.py
@time: 2023/5/23 21:10
@version：Python 3.11.2
@title: 
"""
import socket
import time
from multiprocessing import Process, cpu_count
import os
import re
import traceback
import multiprocessing
import pic_handler
import queue_handler as qe
import byte_stream


class UdpSocket:

    # lst [shared_dict, img_queue, video_queue, rtmp_queue]
    def handle_udp_client(self, sock, process_num, p_queue_dict, lock):
        # 接收和发送UDP数据报
        print(f"启动udp进程:{process_num}")
        while True:
            try:
                data, addr = sock.recvfrom(100000)

                device_id, payload = byte_stream.decode_payload(data)
                p_queue_dict[device_id].put(
                    {'device_id': device_id, 'payload': payload, 'pid': os.getpid(), 'process_num': process_num})

            except Exception as e:
                print("udp接收到处理不了的数据了")
                print(e)
                # 获取异常的详细信息
                traceback_info = traceback.format_exc()
                print(traceback_info)

    def udp(self, p_queue_dict):
        # 创建多进程锁对象
        lock = multiprocessing.Lock()
        # 创建UDP套接字
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_sock.bind(("0.0.0.0", 9090))

        # 判断是否成功启动
        try:
            server_sock.getsockname()
            print("UDP启动成功-prot:6000")
        except socket.error:
            print("UDP服务器启动失败")

        processes = []
        for process_num in range(4):
            # 创建新的进程处理UDP数据报
            process_upd = Process(target=self.handle_udp_client, args=(
                server_sock, process_num, p_queue_dict, lock))
            process_upd.start()
            processes.append(process_upd)

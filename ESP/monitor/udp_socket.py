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


class UdpSocket:

    # lst [shared_dict, img_queue, video_queue, rtmp_queue]
    def handle_udp_client(self, sock, process_num, shared_dict, queue_dict, img_queue, lock):
        # 接收和发送UDP数据报
        print(f"启动udp进程:{process_num}")
        while True:
            try:
                data, addr = sock.recvfrom(100000)
                pic_handler.PicHandler().run(data, shared_dict, queue_dict, img_queue, lock)
                # print(f"udp接收到数据：{data.decode('utf-8')},{str(data)},process_num:{process_num},pid: {os.getpid()}")
                # print(f'device_id:{device_id},process_num:{process_num}, payload:{payload}')
                # response = f"Server response:my pid {os.getpid()},process_num:{process_num}"
                # shared_list[time.time()] = data.decode('utf-8')
                # sock.sendto(response.encode(), addr)
                # print(shared_list)

            except Exception as e:
                print("udp接收到处理不了的数据了")
                print(e)
                # 获取异常的详细信息
                traceback_info = traceback.format_exc()
                print(traceback_info)

    def udp(self, shared_dict, queue_dict):
        img_queue = multiprocessing.Queue()  # 储存照片
        # video_queue = multiprocessing.Queue()  # 储存录像
        # rtmp_queue = multiprocessing.Queue()  # 推流

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

        img_queue_product = multiprocessing.Process(target=qe.save_image, args=(img_queue,))

        processes = []
        for process_num in range(16):
            # 创建新的进程处理UDP数据报
            process_upd = Process(target=self.handle_udp_client, args=(
                server_sock, process_num, shared_dict, queue_dict, img_queue, lock))
            process_upd.start()
            processes.append(process_upd)

        img_queue_product.start()
        # img_queue_product.join()
        #
        # for process_upd in processes:
        #     process_upd.join()

import wlan
from machine import Pin
import network
import socket
import time


'''
启动upd服务器
定义连接WiFi函数
'''
ip = '0.0.0.0'
port = 5000
bufsize = 1024
ttl = 86400

# 启动udp服务器


def start_udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (ip, port)
    server_socket.bind(address)  # 为服务器绑定一个固定的地址，ip和端口
    server_socket.settimeout(ttl)  # 设置一个时间提示，如果10秒钟没接到数据进行提示

    while True:
        receive_data, client = server_socket.recvfrom(bufsize)
        print(receive_data)


def start_tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))

    # 主循环
    while True:
        buf, addr = server_socket.recvfrom(bufsize)
        if buf:
            buf = buf.decode('utf-8')
            print(buf)

import wlan
from machine import Pin
import network
import socket
import time

led = Pin('WL_GPIO0', Pin.OUT)  # 板载LED连到WL_GPIO0
led.value(0)  # 板载LED熄灭

# 定义连接WiFi函数

if wlan.connect_wifi("", ""):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", 5000))

    # 主循环
    while True:
        buf, addr = server_socket.recvfrom(1024)
        if buf:
            buf = buf.decode('utf-8')
            print(buf)
            if buf == "1":
                led.value(1)
            elif buf == "2":
                led.value(0)

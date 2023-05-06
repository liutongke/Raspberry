#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: main.py
@time: 2023/4/27 21:20
@version：Python 3.11.2
@title: 
"""
from machine import Pin
from utime import sleep
import network
import socket
import json
import time
import lightsensitive
import machine
import ssd1306

import machine
import utime
import pcf8591

# i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15), freq=400000)
# I2C_ADDR = i2c.scan()[0]
# print("I2C addr: ", I2C_ADDR)
# pcf = pcf8591.PCF8591(i2c, I2C_ADDR)

# while True:
#     light = pcf.read(0)
#     temp = pcf.read(1)
#     volt = pcf.read(3)

#     print("light: {:d} temperature: {:d} volt: {:d}".format(light, temp, volt))
#     utime.sleep(5)

# http://micropython.circuitpython.com.cn/en/latet/esp8266/tutorial/ssd1306.html
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400_000)
print("I2C设备号：" + str(i2c.scan()[0]))
print(i2c.scan())
display = ssd1306.SSD1306_I2C(128, 64, i2c)


try:
    # oled.text("Raspberry Pi", 0, 0)
    # oled.text("Pico", 80, 10)
    # oled.text("MicroPython", 0, 20)
    # oled.text("OLED(ssd1306)", 0, 40)
    # oled.show()
    display.fill(0)
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(2, 2, 28, 28, 0)
    display.vline(9, 8, 22, 1)
    display.vline(16, 2, 22, 1)
    display.vline(23, 8, 22, 1)
    display.fill_rect(26, 24, 2, 4, 1)
    display.text('MicroPython', 40, 0, 1)
    display.text('SSD1306', 40, 12, 1)
    display.text('OLED 128x64', 40, 24, 1)
    display.line(0, 0, 127, 63, 1)
    display.show()
except KeyboardInterrupt:
    print("stop")
    display.poweroff()
# 通常环境光照度参照表
# https://blog.csdn.net/banrieen/article/details/51190688
while True:
    print(lightsensitive.getLight())
    print(lightsensitive.getLightLux())
    sleep(5)
pin = Pin("WL_GPIO0", Pin.OUT)

print("LED starts flashing...")
while True:
    pin.toggle()
    sleep(1)

# Led灯光显示








# udp操作
class Udp:
    ip = '192.168.1.105'
    port = 8001
    bufsize = 1024
    ttl = 86400

    def send_udp_client_data(self, send_data):
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_client.sendto(send_data, (self.ip, self.port))
        socket_client.close()


# 工具类
class Tools:
    def json_decode(self, json_dict_):
        return json.loads(json_dict_)

    def json_encode(self, dict_):
        return json.dumps(dict_, )


if Wlan().connect_wifi():
    while True:
        Led().blingbling()
        Udp().send_udp_client_data(Tools().json_encode(
            {'light': time.time(), 'cmd': 'null'}))
        sleep(10)

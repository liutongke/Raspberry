#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: PCF8591.py
@time: 2023/4/25 18:19
@version：Python 3.11.2
@title: PCF8591模块 AD/DA转换 模数/温度照度采集 数模转换模块
"""
import smbus
import time

address = 0x48  # address 器件的地址(硬件地址 由器件决定) sudo i2cdetect -y 1 命令查看
A0 = 0x40  # A0 器件某个端口的地址（数据存储的寄存器）
A1 = 0x41
A2 = 0x42
A3 = 0x43
# 0 代表 /dev/i2c-0， 1 代表 /dev/i2c-1 ,具体看使用的树莓派那个I2C来决定
bus = smbus.SMBus(1)  # 开启总线 创建一个smbus实例

# 循环查询
while True:
    # 获取A2端口的数据
    bus.write_byte(address, A2)  # A2端口绑定 发送一个控制字节到设备
    print(bus.read_byte(address))  # 读取A2端口的数据

    time.sleep(1)

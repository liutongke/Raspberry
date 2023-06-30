#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import smbus

# PCF8591的I2C地址
DEVICE_ADDRESS = 0x48

# PCF8591的通道 0光敏电阻模拟信号转化的数字 1电位计模拟信号转化的数字值 2热敏电阻模拟信号转化的数字值
CHANNEL = 0

# 初始化I2C总线
bus = smbus.SMBus(1)


def read_light_intensity():
    # 通过I2C读取PCF8591的光敏电阻值
    bus.write_byte(DEVICE_ADDRESS, 0x40 | CHANNEL)  # 发送命令选择通道和自动转换模式
    time.sleep(0.1)
    light_resistor_value = bus.read_byte(DEVICE_ADDRESS)  # 读取光敏电阻值

    # 根据光敏电阻值计算光照强度
    voltage = light_resistor_value / 255.0 * 3.3  # 假设PCF8591的参考电压为3.3V
    lux = 500 * (3.3 - voltage) / voltage  # 根据光敏电阻的特性曲线计算光照强度

    return round(lux, 2)

# while True:
#     # 读取光照强度并打印结果
#     lux = read_light_intensity()
#     print("光照强度：{} lux".format(lux))

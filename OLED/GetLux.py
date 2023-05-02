#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: PCF8591-test.py
@time: 2023/5/1 1:17
@version：Python 3.11.2
@title: 
"""
# SMBus (System Management Bus,系统管理总线)
import smbus
import time

# https://blog.csdn.net/weixiazailaide/article/details/52782458

__DEV_ADDR = 0x48  # address 器件的地址(硬件地址 由器件决定) sudo i2cdetect -y 1 命令查看

# 控制字
__CMD_PWR_OFF = 0x00  # 关机
__CMD_PWR_ON = 0x01  # 开机
__CMD_RESET = 0x07  # 重置
__CMD_CHRES = 0x10  # 持续高分辨率检测
__CMD_CHRES2 = 0x11  # 持续高分辨率模式2检测
__CMD_CLHRES = 0x13  # 持续低分辨率检测
__CMD_THRES = 0x20  # 一次高分辨率
__CMD_THRES2 = 0x21  # 一次高分辨率模式2
__CMD_TLRES = 0x23  # 一次分辨率
__CMD_SEN100H = 0x42  # 灵敏度100%,高位
__CMD_SEN100L = 0X65  # 灵敏度100%，低位
__CMD_SEN50H = 0x44  # 50%
__CMD_SEN50L = 0x6A  # 50%
__CMD_SEN200H = 0x41  # 200%
__CMD_SEN200L = 0x73  # 200%

bus = smbus.SMBus(1)
bus.write_byte(__DEV_ADDR, __CMD_PWR_ON)
bus.write_byte(__DEV_ADDR, __CMD_RESET)
bus.write_byte(__DEV_ADDR, __CMD_SEN100H)
bus.write_byte(__DEV_ADDR, __CMD_SEN100L)
bus.write_byte(__DEV_ADDR, __CMD_PWR_OFF)


def GetIlluminance():
    bus.write_byte(__DEV_ADDR, __CMD_PWR_ON)
    bus.write_byte(__DEV_ADDR, __CMD_THRES2)
    time.sleep(0.2)
    res = bus.read_word_data(__DEV_ADDR, 0)
    # print(res)
    # read_word_data
    res = ((res >> 8) & 0xff) | (res << 8) & 0xff00
    res = round(res / (2 * 1.2), 2)
    result = "光照强度: " + str(res) + "lx"
    return result

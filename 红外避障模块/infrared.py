#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: infrared.py
@time: 2023/4/20 18:08
@version：Python 3.11.2
@title: 红外避障
"""
import RPi.GPIO as GPIO
import time

GPIO_IN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_IN, GPIO.IN)

try:
    while True:
        # 当模块检测到前方障碍物信号时，电路板上绿色指示灯点亮电平，同时OUT端口持续输出低电平信号
        if GPIO.input(GPIO_IN):
            print("检测到障碍")
        else:
            print("无障碍")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()

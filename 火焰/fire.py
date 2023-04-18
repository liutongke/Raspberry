#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: fire.py
@time: 2023/4/18 13:49
@version：Python 3.11.2
@title: 红外火焰传感器
"""
import RPi.GPIO as GPIO
import time

GPIO_DO = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_DO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
try:
    while True:
        if GPIO.input(GPIO_DO):
            print('没有检测到火焰')
        else:
            print('检测到火焰')
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
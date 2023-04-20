#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: TCRT5000.py
@time: 2023/4/20 18:34
@version：Python 3.11.2
@title: 一路循迹传感器
"""
import RPi.GPIO as GPIO
import time

GPIO_TCRT = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TCRT, GPIO.IN)
try:
    while True:
        status = GPIO.input(GPIO_TCRT)
        print(status)
        if status:
            print('走正了')
        else:
            print('走歪了')
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

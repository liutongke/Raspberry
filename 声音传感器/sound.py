#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: shengyin.py
@time: 2023/4/20 18:38
@version：Python 3.11.2
@title: 声音传感器
"""
import RPi.GPIO as GPIO
import time

GPIO_SOUND = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_SOUND, GPIO.IN)
try:
    while True:
        status = GPIO.input(GPIO_SOUND)
        print(status)
        if status:
            print('静音')
        else:
            print('有声音')
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()

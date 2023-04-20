#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: photoresistor.py
@time: 2023/4/20 18:42
@version：Python 3.11.2
@title: 光敏
"""
import RPi.GPIO as GPIO
import time

GPIO_LIGHT = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_LIGHT, GPIO.IN)
try:
    while True:
        status = GPIO.input(GPIO_LIGHT)
        if status:
            print("有光")
        else:
            print("黑暗")
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()

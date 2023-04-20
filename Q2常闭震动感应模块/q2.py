#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: q2.py
@time: 2023/4/20 14:38
@version：Python 3.11.2
@title: q2 SW-420 常闭型震动模块
"""
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO_Q2 = 18
GPIO.setup(GPIO_Q2, GPIO.IN)

if __name__ == '__main__':
    try:
        while True:
            if GPIO.input(GPIO_Q2):
                print("shake")
                time.sleep(1)
            else:
                print("ok")
                time.sleep(1)
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("bye bye")
        GPIO.cleanup()

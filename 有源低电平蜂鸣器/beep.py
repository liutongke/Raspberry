#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:keke
@file: beep.py
@time: 2023/4/20 13:15
@version：Python 3.11.2
@title: 有源低电平蜂鸣器
"""
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO_BEEP = 18
GPIO.setup(GPIO_BEEP, GPIO.OUT)

GPIO.output(GPIO_BEEP, GPIO.LOW)
time.sleep(5)
GPIO.output(GPIO_BEEP, GPIO.HIGH)
# 脚本运行完毕执行清理工作
GPIO.cleanup()

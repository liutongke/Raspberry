#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import datetime
import picamera
import time

# 如果RPi.GRIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息。你可以通过下列代码禁用警告
GPIO.setwarnings(False)
# 通过红外感应控制灯泡的亮灭
GPIO.setmode(GPIO.BCM)
# 设置蜂鸣器
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)
time.sleep(5)
GPIO.cleanup()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

# 如果RPi.GRIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息。你可以通过下列代码禁用警告
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# 设置pin14负责输出电压
GPIO.setup(14, GPIO.OUT)
# 循环十次结束闪烁
count = 0
while (count < 3):
    # 设置闪烁的函数
    # 输出1
    GPIO.output(14, GPIO.HIGH)
    time.sleep(5)
    # 输出0
    GPIO.output(14, GPIO.LOW)
    time.sleep(5)
    count = count + 1
# 循环结束设置长亮状态
# GPIO.output(14, GPIO.HIGH)
# 清除进程
GPIO.cleanup()

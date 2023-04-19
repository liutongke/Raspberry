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
# 设置pin14负责输出电压亮灯
# GPIO.setup(4, GPIO.OUT)
# 设置蜂鸣器
GPIO.setup(26, GPIO.OUT)
# 设置pin14负责接收红外感应
GPIO.setup(14, GPIO.IN)
# 红外感应器检测到数据，启动（0表示有障碍，1表示没障碍）
count = 5
while count > 0:
    if GPIO.input(14) == int(0):
        # 关闭蜂鸣器
        print('red')
        GPIO.output(26, GPIO.HIGH)
        # GPIO.output(4, GPIO.HIGH)
        time.sleep(0.5)
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            # 摄像头预热1秒
            time.sleep(1)
            # 根据时间戳给照片命名
            stamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
            camera.capture(stamp + '.jpg')
            count = count - 1
    else:
        # 蜂鸣器开启
        print('no red')
        GPIO.output(26, GPIO.LOW)
        time.sleep(1)
        count = count - 1
GPIO.cleanup()

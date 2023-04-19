#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.start_preview()
    # 摄像头预热2秒
    time.sleep(2)
    stamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    camera.capture(stamp + '.jpg')
# import RPi.GPIO as GPIO
# import time
# import datetime
# import picamera
#
# # 如果RPi.GRIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息。你可以通过下列代码禁用警告
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# # 设置pin14负责接收红外感应
# GPIO.setup(14, GPIO.IN)
# # 红外感应器检测到数据，启动（0表示有障碍，1表示没障碍）
# count = 5
# while (count > 0):
#     if (GPIO.input(14) == int(0)):
#         with picamera.PiCamera() as camera:
#             camera.resolution = (1024, 768)
#             camera.start_preview()
#             # 摄像头预热1秒
#             time.sleep(1)
#             # 根据时间戳给照片命名
#             stamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
#             camera.capture(stamp + '.jpg')
#             print ('paisewancheng')
#     count = count - 1
